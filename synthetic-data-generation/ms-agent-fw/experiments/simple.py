import asyncio
import os
from agent_framework.azure import AzureAIClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv
load_dotenv()
async def main():
    project_endpoint = os.getenv("AZURE_AI_PROJECT_ENDPOINT")
    if not project_endpoint:
        raise ValueError("AZURE_AI_PROJECT_ENDPOINT not found in .env")
    
    async with (
        AzureCliCredential() as credential,
        AzureAIClient(credential=credential, endpoint=project_endpoint).as_agent(
            name="Joker",
            instructions="You are good at telling jokes."
        ) as agent,
    ):
        result = await agent.run("Tell me a joke about a Microsoft.")
        print(result.text)

if __name__ == "__main__":
    asyncio.run(main())