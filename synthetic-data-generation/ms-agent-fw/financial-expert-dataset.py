# ---------------------------------------
# Document for multi-turn agent:
# https://learn.microsoft.com/en-us/agent-framework/tutorials/agents/multi-turn-conversation?pivots=programming-language-python 
# ---------------------------------------
import asyncio
from typing import Annotated
import os
import json

from pydantic import Field
from models import UserScenarios
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

@ai_function(name="end_conversation", description="Conversation ending message", return_type=bool)
def end_conversation(
    message: Annotated[str, Field(description="End of the conversation message")],
) -> str:
    return f"TERMINATE: {message}"

async def main():
    endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    user_scenarios = load_scenarios("scenarios.json")
    final_dataset = []
    max_turns = 10 # Maximun conversation turns per scenario
    for entry in user_scenarios[0:3]:  # Limit to first 3 personas for testing
        async with AzureCliCredential() as credential:
            chat_client = AzureAIClient(endpoint=endpoint, credential=credential)
            persona = entry.user
            user = chat_client.as_agent(
                    name="SimulatedUser",
                    instructions=f"You are {persona.full_name}, a person with this persona: {persona}."
                    f"You are currently feeling '{persona.persona_mood}. Respond naturally and ask follow-up questions if needed.' "
                    f"When you have all the advise or you don't have any more questions, respond with a message indicating that to end the conversation with the advisor.",
                    )
            for topic in entry.scenarios:   
                advisor = chat_client.as_agent(
                        name="FinancialAdvisor",
                        instructions=(
                            "You are a senior financial advisor in stock investment. You help users to make informed investment decisions that support their financial goals. Your role is to provide personalized financial advice, answer user questions, and guide them through various investment strategies. You must ensure that your advice is accurate, relevant, and compliant with financial regulations while maintaining a friendly and approachable tone. Your interactions should help users feel confident in their investment choices and foster long-term relationships. You ensure that the advisor can effectively address user needs and provide valuable financial advice in stock investment."
                            "Your job is to provide financial advice to users based on their unique personas and scenarios. "
                            "You should consider their financial background, goals, and challenges when giving advice. "
                            f"Currently, you are engaging with user {persona.full_name} who is {persona.age} years old and works as a {persona.occupation} in {persona.location}. "
                            "Engage in multi-turn conversations, ask clarifying questions, and tailor your advice to user's needs. Provide clear and meaningful, thoughtful responses. "
                            "Avoid misleading or harmful advise. If you are unsure about a user's request, ask for more information rather than making assumptions. "
                            "If user asks inappropriate or harmful questions, politely refuse to answer and redirect the conversation to financial topics. "
                            "ALWAYS consider the risks associated with investment advise and clearly communicate them to the user. "
                            "You ensure that all advice provided adheres to legal and ethical standards of either US or UK based on users' respective locations. "
                            "You also ensure that the advise is not misleading, avoid suggesting a hope and promise of high returns, and was giving with proper disclosures. "
                            f""" 
                            - You don't need to address the user by name in every turn and it will make the conversation more natural
                            - You can ask questions, provide clarifications, and offer suggestions to guide the conversation.
                            - Never sound artificial or robotic.
                            - You cannot express promise such as 'I will do that' or 'I promise the stock will perform well'.
                            - ALWAYS prioritize safety: remind the user about investment risks and uncertainties when providing advice.
                            - Use clear and simple language suitable for the user's financial literacy level.
                            - Avoid jargon and technical terms unless the user demonstrates understanding.
                            - Provide balanced advice considering both short-term and long-term financial goals.
                            - If the user provides extra information, incorporate it into your advice appropriately.
                            - Ensure ethical standards in all responses.
                            - Ensure compliance with financial regulations specific to the user's location.
                            """
                            f"""IMPORTANT: When the user indicates they are done (e.g., says goodbye, thank you, no more questions), 
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
                    f"You are {topic.persona_mood}. Start a discussion with financial advisor on {topic.title}."
                )
                message_logs = []
                
                conversation_ended = False
   
                async for event in workflow.run_async(initial_prompt):
                    if isinstance(event, WorkflowOutputEvent):
                        msg = event.output

                        if "TERMINATE:" in msg.text:
                            text = msg.text.replace("TERMINATE:", "").strip()
                            msg.text = text
                            conversation_ended = True
                        message_logs.append(msg)
                        if conversation_ended:
                            break
                    if len(message_logs) >= max_turns:
                        break
                formatted_dialogue = []
                for msg in message_logs:
                    if msg.author_name == "SimulatedUser":
                        formatted_dialogue.append({"role": "user", "content": msg.text})
                    elif msg.author_name == "FinancialAdvisor":
                        formatted_dialogue.append({"role": "assistant", "content": msg.text})
                
                if formatted_dialogue:
                    final_dataset.append({"messages": formatted_dialogue})


    with open("synthetic_financial_dialogue.jsonl", "w") as f:
        for entry in final_dataset:
            f.write(json.dumps(entry) + "\n")

if __name__ == "__main__":
    asyncio.run(main())