#!/usr/bin/env python
from random import randint

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from crewai.flow import Flow, listen, start

from conv_flow.crews.user_research_crew.user_research_crew import UserResearchCrew
from conv_flow.crews.scenario_crew.scenario_crew import ScenarioCrew

# Define models for structured data
class Persona(BaseModel):
    username: str = Field(description="username of the persona")
    full_name: str = Field(description="full name of the persona")
    age: int = Field(description="age of the persona")
    occupation: str = Field(description="occupation of the persona")
    goals: List[str] = Field(description="goals of the persona")
    challenges: List[str] = Field(description="challenges faced by the persona")
    gender: str = Field(description="gender of the persona")
    location: str = Field(description="location of the persona in US or UK")
    marital_status: str = Field(description="marital status of the persona")
    interests: List[str] = Field(description="interests and hobbies of the persona")
    speech_style: str = Field(description="speech style of the persona")
    financial_background: str = Field(description="financial background of the persona and financial literacy level, experience with investing")
    attitude: str = Field(description="attitude towards money and investing of the persona")
    qualities: str = Field(description="personal qualities summarizing their character and persona's attitude. Avoid getting too witty, as doing so may taint the persona as being too fun and not a useful tool")
    risk_tolerance: str = Field(description="investment risk tolerance level of the persona")
    extra_info: Optional[Dict[str, str]] = Field(description="any extra useful information about the persona, or memory of past experiences with financial advisors and investing")
    image_prompt: str = Field(description="prompt to generate an image representing the persona")

class PersonaList(BaseModel):
    personas: List[Persona] = Field(description="List of user personas")

class Scenario(BaseModel):
    persona: Persona = Field(description="Persona used in the scenario")
    title: str = Field(description="Title of the scenario")
    introduction: str = Field(description="Introduction to the topic")
    description: str = Field(description="Detailed description of the scenario")
    context: List[Persona] = Field(description="Topic context to trigger the discussion with the financial advisor")
    history: Optional[str] = Field(description="previous conversation history with the financial advisor if any")
    persona_mood: str = Field(description="current mood of the persona")

class ScenarioList(BaseModel):
    scenarios: List[Scenario] = Field(description="List of user research scenarios")

class GenState(BaseModel):
    sentence_count: int = 1
    poem: str = ""


class UXFlow(Flow[GenState]):

    @start()
    def ux_research(self):
        # Run the content crew for this section
        result = UserResearchCrew().crew().kickoff()
        print("UX research completed", result.raw)
        return result.raw

    @listen(ux_research)
    def scenario_development(self, research_output: str):
        print("Creating personas")
        result = (
            ScenarioCrew()
            .crew()
            .kickoff(inputs={"research_result": research_output})
        )

        print("Scenario generated", result.raw)
        return result.pydantic()


def kickoff():
    ux_flow = UXFlow()
    ux_flow.kickoff()

def plot():
    ux_flow = UXFlow()
    ux_flow.plot()


def run_with_trigger():
    """
    Run the flow with trigger payload.
    """
    import json
    import sys

    # Get trigger payload from command line argument
    if len(sys.argv) < 2:
        raise Exception("No trigger payload provided. Please provide JSON payload as argument.")

    try:
        trigger_payload = json.loads(sys.argv[1])
    except json.JSONDecodeError:
        raise Exception("Invalid JSON payload provided as argument")

    # Create flow and kickoff with trigger payload
    # The @start() methods will automatically receive crewai_trigger_payload parameter
    ux_flow = UXFlow()

    try:
        result = ux_flow.kickoff({"crewai_trigger_payload": trigger_payload})
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the flow with trigger: {e}")


if __name__ == "__main__":
    kickoff()
