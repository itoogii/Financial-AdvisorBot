# Original: https://github.com/Azure-Samples/python-openai-demos/blob/main/chat_history_stream.py
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

import azure.identity
import openai


# updated to use pydantic-settings instead of dotenv.
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    GITHUB_TOKEN: str
    GITHUB_MODEL: str = "meta/Meta-Llama-3.1-8B-Instruct"
    API_HOST: Optional[str] = None
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_CHAT_DEPLOYMENT: Optional[str] = None
    OLLAMA_ENDPOINT: Optional[str] = None
    OLLAMA_MODEL: Optional[str] = None
    OPENAI_KEY: Optional[str] = None
    OPENAI_MODEL: Optional[str] = None


settings = Settings()
GITHUB_TOKEN = settings.GITHUB_TOKEN
API_HOST = settings.API_HOST

# Setup the OpenAI client to use either Azure, OpenAI.com, or Ollama API


if API_HOST == "ollama":
    client = openai.OpenAI(base_url=settings.OLLAMA_ENDPOINT, api_key="nokeyneeded")
    MODEL_NAME = settings.OLLAMA_MODEL
else:
    client = openai.OpenAI(
        base_url="https://models.github.ai/inference",
        api_key=settings.GITHUB_TOKEN,
    )
    MODEL_NAME = settings.GITHUB_MODEL


messages = [
    {
        "role": "system",
        "content": 'Instruction: You are a conversational designer. You are building a chatbot to help users find information about their insurance claims. Insurance claims include the following information: a claim date, a member ID, and a claim amount. Generate conversational responses until you have collected all three pieces of information. When you have all the information, respond with a  payload in this format: {"memberID": "(the member id collected)", "claimDate": "(the claim date collected)", "claimAmount": "(the claim amount collected)"}',
    },
]

while True:
    question = input("\nYour question: ")
    print("Sending question...")

    messages.append({"role": "user", "content": question})
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.7,
        stream=True,
        max_tokens=1000,
    )

    print("\nAnswer: ")
    bot_response = ""
    for event in response:
        if event.choices and event.choices[0].delta.content:
            content = event.choices[0].delta.content
            print(content, end="", flush=True)
            bot_response += content
    print("\n")
    messages.append({"role": "assistant", "content": bot_response})
