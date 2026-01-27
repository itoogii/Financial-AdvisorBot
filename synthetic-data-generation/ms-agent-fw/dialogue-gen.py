# ---------------------------------------
# Document for multi-turn agent:
# https://learn.microsoft.com/en-us/agent-framework/tutorials/agents/multi-turn-conversation?pivots=programming-language-python 
# ---------------------------------------
import asyncio
from typing import Annotated, Any, cast
import os
import json
from collections.abc import Awaitable, Callable
from contextlib import AsyncExitStack

from pydantic import Field
from models import UserScenarios
from agent_framework.ollama import OllamaChatClient 
# from agent_framework.openai import OpenAIChatClient
from agent_framework import (
    ChatMessage,
    ChatAgent,
    Role,
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

def smart_selector(state: GroupChatState) -> str:
    """Select speakers based on conversation content and context."""
    conversation = state.conversation

    last_message = conversation[-1] if conversation else None

    # If no messages yet, start with SimulatedUser
    if not last_message:
        return "SimulatedUser"

    # Check last message content
    last_text = last_message.text.lower()

    # after SimulatedUser responded, switch to FinancialAdvisor
    if "I have finished" in last_text and last_message.author_name == "SimulatedUser":
        return "FinancialAdvisor"

    # Else continue with researcher until it indicates completion
    return "SimulatedUser"

def round_robin_selector(state: GroupChatState) -> str:
    """A round-robin selector function that picks the next speaker based on the current round index."""
    participant_names = list(state.participants.keys())
    speaker = participant_names[state.current_round % len(participant_names)]
    print(f"[Selector] Round {state.current_round}: selected speaker is {speaker}")
    return speaker

async def main():
   
    user_scenarios = load_scenarios("scenarios.json")
    final_dataset = []
    max_turns = 6 # Maximun conversation turns per scenario
     # Create orchestrator agent for speaker selection
    # agent_factory, close = await create_azure_ai_agent()

        
    for entry in [user_scenarios[0]]:  # Limit to first persona for testing
        for topic in [entry.scenarios[0]]: 
            persona = entry.user
            print("=" * 80)
            print(f"{persona.full_name} to discuss {topic.title}")
            agent_factory, close = await create_azure_ai_agent()
            try:
                user = await agent_factory(
                        name="SimulatedUser",
                        instructions=f"""You are {persona.full_name}, a person with this persona: {persona}.
                        As a human you talk realistically with financial advisor in a conversational manner.
                        You don't ask all your questions at once, instead you make conversation as a real person and wait for the advisor's response before continuing the conversation.
                        You may provide additional information about your situation as needed and you may ask follow-up questions based on the advisor's responses.
                        Your goal is to get financial advice until you are satisfied with the information provided and think you have enough.
                        When you are done and you don't have any more questions, respond by indicating to end the conversation.""",
                        )
                
                advisor = await agent_factory(
                        name="FinancialAdvisor",
                        instructions=(
                            f"""You are a senior financial advisor in stock investment. As an advisor you talk realistically with your user in a conversational manner. You answer user questions, and provide meaningful and thoughtful financial advice. You ensure effectively address user needs and provide valuable financial advice in stock investment.
                            Currently, you are engaging with user named {persona.full_name} who is {persona.age} years old and works as a {persona.occupation} in {persona.location}.  
                            If you are unsure about a user's request, ask for more information rather than making assumptions. 
                            If the content is inappropriate or harmful, politely refuse to answer and redirect the conversation to financial topics. 
                            - You don't need to address the user by name in every turn and it will make the conversation more natural. Don't use slang or overly casual language. Be professional yet approachable.
                            - You can ask questions, provide clarifications, and offer suggestions to guide the conversation in respective tone.
                            - Never sound artificial or robotic.
                            - You cannot express promise such as 'I will do that' or 'I promise the stock will perform well'.
                            - ALWAYS prioritize safety: remind the user about investment risks and uncertainties when providing advice.
                            - Avoid jargon and technical terms unless the user demonstrates understanding.
                            - Provide balanced advice considering both short-term and long-term financial goals.
                            - If the user provides extra information, incorporate it into your advice appropriately.
                            - Ensure ethical standards in all responses.
                            - Ensure all advice provided adheres to legal and ethical standards of either US or UK based on users' respective locations
                            IMPORTANT: When the user indicates they are done (e.g., says goodbye, thank you, no more questions), 
                            """
                        ),
                    )  
                
                workflow = (GroupChatBuilder()
                    .with_select_speaker_func(round_robin_selector)
                    # Set a hard termination condition: stop after 7 assistant messages
                    # The agent orchestrator will intelligently decide when to end before this limit but just in case
                    .participants([user, advisor])
                    .with_termination_condition(lambda conversation: len(conversation) >= 7)
                    .build()
                )

                task = (
                    f"{topic.description}. '{topic.trigger_event}' triggered the SimulatedUser to seek advice. "
                    f"{'SimulatedUser remembers ' + topic.history if topic.history else ''} "
                    f"SimulatedUser is feeling {topic.persona_mood}. SimulatedUser engages a discussion with financial advisor on {topic.title}. SimulatedUser starts the conversation..."
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
                    if msg.author_name == "SimulatedUser":
                        formatted_dialogue.append({"role": "user", "content": msg.text})
                    elif msg.author_name == "FinancialAdvisor":
                        formatted_dialogue.append({"role": "assistant", "content": msg.text})
                
                if formatted_dialogue:
                    final_dataset.append({"messages": formatted_dialogue})
            finally:
                await close()
                # pass
                
    with open("synthetic_financial_dialogue.jsonl", "w") as f:
        for entry in final_dataset:
            f.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    asyncio.run(main())