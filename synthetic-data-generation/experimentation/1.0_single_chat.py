# Original: https://github.com/Azure-Samples/python-openai-demos/blob/main/chat.py
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
import azure.identity
import openai


# updated to use pydantic-settings instead of dotenv.
class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    GITHUB_TOKEN: str
    GITHUB_MODEL: str = "meta/Meta-Llama-3.1-8B-Instruct"
    API_HOST: str = "github"
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
### I am using pydandic-settings to load the .env file for the GitHub token.


# API_HOST = os.getenv("API_HOST", "github")

if API_HOST == "azure":
    if not settings.AZURE_OPENAI_ENDPOINT or not settings.AZURE_OPENAI_CHAT_DEPLOYMENT:
        raise ValueError(
            "AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_CHAT_DEPLOYMENT are required."
        )
    token_provider = azure.identity.get_bearer_token_provider(
        azure.identity.DefaultAzureCredential(),
        "https://cognitiveservices.azure.com/.default",
    )
    client = openai.OpenAI(
        base_url=settings.AZURE_OPENAI_ENDPOINT,
        api_key=token_provider,
    )
    MODEL_NAME = settings.AZURE_OPENAI_CHAT_DEPLOYMENT

elif API_HOST == "ollama":
    if not settings.OLLAMA_ENDPOINT or not settings.OLLAMA_MODEL:
        raise ValueError("OLLAMA_ENDPOINT and OLLAMA_MODEL are required.")
    client = openai.OpenAI(base_url=settings.OLLAMA_ENDPOINT, api_key="nokeyneeded")
    MODEL_NAME = settings.OLLAMA_MODEL
elif API_HOST == "github":
    client = openai.OpenAI(
        base_url="https://models.github.ai/inference",
        api_key=GITHUB_TOKEN,
    )
    MODEL_NAME = settings.GITHUB_MODEL

else:
    if not settings.OPENAI_KEY or not settings.OPENAI_MODEL:
        raise ValueError("OPENAI_KEY and OPENAI_MODEL are required.")
    client = openai.OpenAI(api_key=settings.OPENAI_KEY)
    MODEL_NAME = settings.OPENAI_MODEL


response = client.chat.completions.create(
    model=MODEL_NAME,
    temperature=0.7,
    max_tokens=1000,
    messages=[
        {
            "role": "system",
            "content": "You are a financial advisor that helps people make better financial decisions.",
        },
        {"role": "user", "content": "Should I invest in AAPL?"},
    ],
)

print(f"Response from {API_HOST}: \n")
print(response.choices[0].message.content)
