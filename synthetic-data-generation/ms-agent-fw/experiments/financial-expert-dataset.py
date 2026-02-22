# ---------------------------------------
# Document for multi-turn agent:
# https://learn.microsoft.com/en-us/agent-framework/tutorials/agents/multi-turn-conversation?pivots=programming-language-python 
# ---------------------------------------
import asyncio
from typing import Annotated, Any
import os
import json
from collections.abc import Awaitable, Callable
from contextlib import AsyncExitStack

from pydantic import Field
from models import UserScenarios
from agent_framework.ollama import OllamaChatClient 
# from agent_framework.openai import OpenAIChatClient
from agent_framework import (
    ai_function,

    WorkflowBuilder,
    WorkflowOutputEvent,

)
from agent_framework.azure import AzureAIClient, AzureAIAgentClient
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

async def main():
    
    user_scenarios = load_scenarios("scenarios.json")
    final_dataset = []
    max_turns = 10 # Maximun conversation turns per scenario
    for entry in user_scenarios[0:3]:  # Limit to first 3 personas for testing
        for topic in entry.scenarios:  
            persona = entry.user
            print(f"{persona.full_name} wants to discuss {topic.title}")
            agent, close = await create_azure_ai_agent()
            try:
                user = OllamaChatClient().as_agent(
                        name="SimulatedUser",
                        instructions=f"You are {persona.full_name}, a person with this persona: {persona}."
                        f"Respond naturally and ask follow-up questions if needed. "
                        f"When you are done, got all the advice you need or you don't have any more questions, respond with a message indicating that to end the conversation with the advisor.",
                        )
                
                advisor = OllamaChatClient().as_agent(
                        name="FinancialAdvisor",
                        instructions=(
                            f"""You are a senior financial advisor in stock investment. You help users to make informed investment decisions that support their financial goals. Your role is to provide personalized financial advice, answer user questions, and guide them through various investment strategies. You ensure that the advisor can effectively address user needs and provide valuable financial advice in stock investment.
                            Currently, you are engaging with user {persona.full_name} who is {persona.age} years old and works as a {persona.occupation} in {persona.location}. 
                            Provide clear and meaningful, thoughtful responses. 
                            Avoid misleading or harmful advise. If you are unsure about a user's request, ask for more information rather than making assumptions. 
                            If user asks inappropriate or harmful questions, politely refuse to answer and redirect the conversation to financial topics. 
                            - You don't need to address the user by name in every turn and it will make the conversation more natural.
                            - You can ask questions, provide clarifications, and offer suggestions to guide the conversation in respective tone.
                            - Never sound artificial or robotic.
                            - You cannot express promise such as 'I will do that' or 'I promise the stock will perform well'.
                            - ALWAYS prioritize safety: remind the user about investment risks and uncertainties when providing advice.
                            - Use clear and simple language suitable for the user's financial literacy level.
                            - Avoid jargon and technical terms unless the user demonstrates understanding.
                            - Provide balanced advice considering both short-term and long-term financial goals.
                            - If the user provides extra information, incorporate it into your advice appropriately.
                            - Ensure ethical standards in all responses.
                            - Ensure all advice provided adheres to legal and ethical standards of either US or UK based on users' respective locations
                            IMPORTANT: When the user indicates they are done (e.g., says goodbye, thank you, no more questions), 
                            you MUST call the 'end_conversation' tool with a polite closing message to gracefully end the dialogue."""
                        ),
                        tools=[end_conversation],
                    )  
                
                workflow = (
                        WorkflowBuilder()
                        .set_start_executor(user)
                        .add_edge(user, advisor)
                        .add_edge(advisor, user)
                        .build()
                    )
                initial_prompt = (
                    f"{topic.description}. '{topic.trigger_event}' has happened and this triggered you to seek advice. "
                    f"{'You remember ' + topic.history if topic.history else ''} "
                    f"You are feeling {topic.persona_mood}. Start a discussion with financial advisor on {topic.title}."
                )
                message_logs = []
                
                conversation_ended = False
                print("  Starting conversation now...\n")
                async for event in workflow.run_stream(initial_prompt):
                    print(f"Event received: {event}")
                    if isinstance(event, WorkflowOutputEvent):
                        msg = event.output
                        print(f"message: {str(msg)}")
                        if "TERMINATE:" in msg.text:
                            text = msg.text.replace("TERMINATE:", "").strip()
                            msg.text = text
                            conversation_ended = True
                        message_logs.append(msg)
                        if conversation_ended:
                            break
                    if len(message_logs) >= max_turns:
                        break
                    # await asyncio.sleep(2)
                formatted_dialogue = []
                for msg in message_logs:
                    if msg.author_name == "SimulatedUser":
                        formatted_dialogue.append({"role": "user", "content": msg.text})
                    elif msg.author_name == "FinancialAdvisor":
                        formatted_dialogue.append({"role": "assistant", "content": msg.text})
                
                if formatted_dialogue:
                    final_dataset.append({"messages": formatted_dialogue})
            finally:
                await close()
            
    with open("synthetic_financial_dialogue.jsonl", "w") as f:
        for entry in final_dataset:
            f.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    asyncio.run(main())