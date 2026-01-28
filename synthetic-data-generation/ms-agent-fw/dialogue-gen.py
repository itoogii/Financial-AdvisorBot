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
    return speaker

async def main():
   
    user_scenarios = load_scenarios("scenarios.json")
    max_turns = 11 # Maximun conversation turns - should be odd number to end with advisor, it would be rude if advisor stops abruptly all the time
    # Create orchestrator agent for speaker selection
    # agent_factory, close = await create_azure_ai_agent()
    for entry in user_scenarios[9:]: # I partially completed earlier and added the 1.5s sleep to fix rate limit errors
        persona = entry.user
        for topic in entry.scenarios:
            start = time.time()
            agent_factory, close = await create_azure_ai_agent()
            try:
                user = await agent_factory(
                        name="Customer",
                        instructions=f"""You are {persona.full_name}. Your personality, speech style and persona is defined as: {persona}. Be sure to embody this persona in your responses.
                        As a customer, you are seeking advice from the financial advisor in a conversational manner for the scenario and situation you are currently facing.
                        You start a conversation with the advisor. You may begin with a greeting based on your personality and mood, otherwise you may start with your first question. Wait for the advisor's response before continuing the conversation. You don't need to be overly wordy, just be natural and realistic.
                        You may provide additional information about your situation if needed. You may ask follow-up questions based on the advisor's responses.
                        Your goal is to get financial advice for your current situation until you are satisfied with the information provided and think you have enough.
                        Aim to finish the conversation within {max_turns} turns.
                        When you are done and you don't have any more questions, respond by indicating to end the conversation.""",
                        )
                
                advisor = await agent_factory(
                        name="FinancialAdvisor",
                        instructions=(
                            f"""You are financial advisor named Hermes. You are expert in providing meaningful and thoughtful financial advice in stock investment.
                            Currently, you are engaging with user named {persona.full_name} who is {persona.age} years old and works as a {persona.occupation} in {persona.location} in a conversation.  
                            If you are unsure about a user's request, ask for clarifications rather than making assumptions. 
                            If the content is inappropriate or harmful, politely refuse to answer and redirect the conversation to financial topics. 
                            - You don't need to address the user by name in every turn and it will make the conversation more natural. 
                            - You can ask questions, provide clarifications, and offer suggestions to guide the conversation in respective tone.
                            - Never sound artificial or robotic. Be realistic and natural in your responses.
                            - You cannot express promise such as 'I will do that' or 'I promise the stock will perform well'.
                            - ALWAYS prioritize safety: remind the user about investment risks and uncertainties when providing advice.
                            - Avoid jargon and technical terms unless the user demonstrates understanding.
                            - Provide balanced advice considering both short-term and long-term financial goals.
                            - If the user provides extra information, incorporate it into your advice appropriately.
                            - Ensure ethical standards in all responses. Don't use slang or overly casual language. Be professional yet approachable.
                            - Ensure all advice provided adheres to legal and ethical standards of either US or UK based on users' respective locations
                            IMPORTANT: When the user indicates they are done (e.g., says goodbye, thank you, no more questions), respond with a concise closing statement and end the conversation 
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
                        await asyncio.sleep(2) # adding delay to avoid rate limit errors
                    elif isinstance(event, WorkflowOutputEvent):
                        # Workflow completed - data is a list of ChatMessage
                        final_conversation = cast(list[ChatMessage], event.data)
                # print(f"\nFinal conversation: {dir(final_conversation[0])}\n")
                # print(f"\n{final_conversation[0].author_name}: {final_conversation[0].text}\n")
                # print(f"\n{final_conversation[1].author_name}: {final_conversation[1].text}\n")
                # print(f"\n{final_conversation[2].author_name}: {final_conversation[2].text}\n")
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