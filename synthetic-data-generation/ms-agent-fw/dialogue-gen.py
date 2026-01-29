# ---------------------------------------
# Document for multi-turn agent:
# https://learn.microsoft.com/en-us/agent-framework/tutorials/agents/multi-turn-conversation?pivots=programming-language-python 
# Used the all available information from MAF documentation and tutorials to build this script.
# ---------------------------------------
import asyncio
import time
from typing import Annotated, Any, cast
import os
import json
from collections.abc import Awaitable, Callable
from contextlib import AsyncExitStack

from pydantic import Field
from models import UserScenarios

# from agent_framework.openai import OpenAIChatClient
from agent_framework import (
    ChatMessage,
    ai_function,
    GroupChatBuilder, 
    GroupChatState,
    WorkflowOutputEvent,
    AgentResponseUpdate

)
from agent_framework.azure import AzureAIClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

# Load the scenarios and make it pydantic objects
def load_scenarios(file_path: str) -> list[UserScenarios]:
    with open(file_path, "r") as f:
        data = json.load(f)
    scenarios = [UserScenarios.model_validate(entry) for entry in data]
    return scenarios

# Record the conversations to the file. Using the same method as in conv_flow/main.py
def record_conversations(conversations):
        if os.path.exists("dialogue-dataset.jsonl"):
            try:
                with open("dialogue-dataset.jsonl", "a") as file:
                    file.write(json.dumps(conversations) + "\n")
            except Exception as e:
                print(f"Unable to append dialogue-dataset.jsonl: {e}")
        else:
            # Writing new scenarios to the scenarios file
            with open("dialogue-dataset.jsonl", "w") as file:
                file.write(json.dumps(conversations) + "\n")


async def create_azure_ai_agent() -> tuple[Callable[..., Awaitable[Any]], Callable[[], Awaitable[None]]]:
    """Helper method to create an Azure AI agent factory and a close function.
    This makes sure the async context managers are properly handled.
    """
    endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    stack = AsyncExitStack()
    cred = await stack.enter_async_context(AzureCliCredential())
    client = await stack.enter_async_context(AzureAIClient(endpoint=endpoint, credential=cred))
    async def agent(**kwargs: Any) -> Any:
        return await stack.enter_async_context(client.as_agent(**kwargs))

    async def close() -> None:
        await stack.aclose()
    return agent, close


@ai_function(name="end_conversation", description="Conversation ending message")
def end_conversation(
    message: Annotated[str, Field(description="End of the conversation message")],
) -> str:
    return f"TERMINATE: {message}"

def round_robin_selector(state: GroupChatState) -> str:
    """A round-robin selector function that picks the next speaker based on the current round index."""
    participant_names = list(state.participants.keys())
    speaker = participant_names[state.current_round % len(participant_names)]
    print(f"[Selector] Round {state.current_round}: selected speaker is {speaker}")
    time.sleep(5)
    return speaker

async def main():
   
    user_scenarios = load_scenarios("scenarios.json")
    max_turns = 9 # Maximun conversation turns - should be odd number to end with advisor, it would be rude if advisor stops abruptly all the time
    # Create orchestrator agent for speaker selection
    # agent_factory, close = await create_azure_ai_agent()
    for entry in user_scenarios[38:]: # I partially completed earlier and added the 1.5s sleep to fix rate limit errors
        persona = entry.user
        for topic in entry.scenarios:
            start = time.time()
            agent_factory, close = await create_azure_ai_agent()
            try:
                user = await agent_factory(
                        name="Customer",
                        instructions=f"""
                        Role: You are {persona.full_name}. Your personality and background are: {persona}.
                        Objective: Start and maintain a conversation with a financial advisor named Hermes to resolve your current financial situation.
                        STRICT Interaction Rules:
                        - Single Turn Only: You must ONLY output one response for {persona.full_name}.
                        - No Hallucinating Advisor: Never write, predict, or answer on behalf of Hermes. Your response must end immediately after your persona finishes speaking.
                        - Conciseness: Be natural and realistic. Do not be overly wordy.
                        - Goal-Oriented: Ask follow-up questions until you feel your specific situation is addressed. Aim to conclude the interaction within {max_turns//2} turns.
                        General Guidelines:
                        - Start: Begin the conversation by greeting Hermes and explaining your situation. Stop and wait for Hermes to respond. Continue ONLY after Hermes replies.
                        - Termination: Once satisfied, indicate the conversation is over to Hermes and stop.
                        - Clarity: If a response from Hermes is unclear, you can ask for clarification before proceeding.
                        - Natural and organic conversation: You may avoid addressing Hermes by name in every response. For instance, you can say "I think that's a great idea" that sounds more natural than "I think that's a great idea, John." This creates a more organic flow." 
                        """,
                        ) # Last prompt came from ConvoGen paper
                
                advisor = await agent_factory(
                        name="FinancialAdvisor",
                        instructions=(
                            f"""
                                Role: You are Hermes, a professional financial advisor specializing in stock investments.
                                Objective: Engage with {persona.full_name} ({persona.age}, {persona.occupation}, based in {persona.location}). Provide meaningful, balanced, and ethical financial advice.
                                General Guidelines:
                                - You are the expert. If the user suggests their own answers or seems confused, gently correct them and provide the professional perspective.
                                - ALWAYS prioritize risk disclosure. Remind the user of market uncertainties.
                                - Be professional yet approachable, natural and realistic. Avoid jargon unless the user is clearly knowledgeable. Avoid slang or overly casual language.
                                - Adhere to {persona.location} (US/UK) legal and ethical standards.
                                - If the user signals the end of the conversation (For instance: "Thank you," "Goodbye"), provide a concise closing and stop.
                                - Clarity: If a request is unclear, ask for clarification before advising. Redirect the conversation back to financial topics if it diverts.
                                - Avoid hallucination: Your response must end immediately after you finish speaking.
                                - Natural and organic conversation: You may avoid addressing user by name in every response. For instance, you can say "I think that's a great idea" that sounds more natural than "I think that's a great idea, John." This creates a more organic flow." 
                            """
                        ),
                    )  
                
                workflow = (GroupChatBuilder()
                    .with_select_speaker_func(round_robin_selector)
                    # Set a hard termination condition: stop after 7 assistant messages
                    # The agent orchestrator will intelligently decide when to end before this limit but just in case
                    .participants([user, advisor])
                    .with_termination_condition(lambda conversation: len(conversation) >= max_turns)
                    .build()
                )
                print("=" * 80)
                print(f"{persona.full_name} to discuss {topic.title}")

                task = (
                    f"""{topic.description}. '{topic.trigger_event}' triggered the customer to seek advice. 
                    {'Customer remembers ' + topic.history if topic.history else ''} 
                    Customer is feeling {topic.persona_mood}. Customer starts the conversation to discuss {topic.title}"""
                )
                
                final_conversation: list[ChatMessage] = []
                last_executor_id: str | None = None

                # Run the workflow
                async for event in workflow.run_stream(task):
                    if isinstance(event, AgentResponseUpdate):
                        # Print streaming agent updates
                        eid = event.executor_id
                        if eid != last_executor_id:
                            if last_executor_id is not None:
                                print()
                            print(f"[{eid}]:", end=" ", flush=True)
                            last_executor_id = eid
                        print(event.data, end="", flush=True)
                        print("Async delay 5 seconds...")
                        await asyncio.sleep(5) # adding delay to avoid rate limit errors. Increased to 5s as it hits maximum tokens limit for long conversations
                    elif isinstance(event, WorkflowOutputEvent):
                        # Workflow completed - data is a list of ChatMessage
                        final_conversation = cast(list[ChatMessage], event.data)
                        await asyncio.sleep(10)

                if final_conversation:
                    print("\n\n" + "=" * 80)
                    print("Final Conversation:")
                    for msg in final_conversation:
                        author = getattr(msg, "author_name", "Unknown")
                        text = getattr(msg, "text", str(msg))
                        print(f"\n[{author}]\n{text}")
                        print("-" * 80)
                
                formatted_dialogue = []
                for msg in final_conversation:
                    if msg.author_name == "Customer":
                        formatted_dialogue.append({"role": "user", "content": msg.text})
                    elif msg.author_name == "FinancialAdvisor":
                        formatted_dialogue.append({"role": "assistant", "content": msg.text})

                #conversations is an object dict {"messages": [{}, {}, {}]}
                record_conversations({"messages": formatted_dialogue})
                
            except Exception as e:
                print(f"Error occured for '{topic.title}': {e}")   
            finally:
                await close()
                time.sleep(3) # Adding delay 3 seconds to prevent rate limit errors
            end = time.time()
            print("\n" + "=" * 80 )
            duration = end - start
            print(f"Total time to generate topic '{topic.title}': {duration} seconds")
            pause = 60 - duration
            if pause > 0:
                print("\n" + "=" * 80 )
                print(f"Pausing for {pause} seconds to avoid 'Too Many Requests' errors...")
                time.sleep(pause) # I was still having "Too Many Requests" errors on AzureCLI. So making the one iteration to be at least 60 seconds
                print("\n" + "=" * 20 + " Resuming " + "=" * 20 )
        
                
if __name__ == "__main__":
    asyncio.run(main())