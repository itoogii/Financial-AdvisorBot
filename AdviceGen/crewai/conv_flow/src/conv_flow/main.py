#!/usr/bin/env python
from pydantic import BaseModel, ValidationError
from typing import Optional, List
from crewai.flow import Flow, listen, start

from conv_flow.crews.user_research_crew.user_research_crew import UserResearchCrew
from conv_flow.crews.scenario_crew.scenario_crew import ScenarioCrew

from conv_flow.models import PersonaList, Scenario

import os

# Defined the state to hold the data
class GenState(BaseModel):
    message: str = ""
    personas: Optional[PersonaList] = None



class UXFlow(Flow[GenState]):
    def __init__(self):
        super().__init__()
        # since my flow kickoff was failing in scenario crew, I decided to load existing personas here
        # in case it exists.
        print(f"Current working directory: {os.getcwd()}")
        if os.path.exists("personas.json"):
            print("Personas file exists")
            try:
                with open("personas.json", "r") as file:
                    self.state.personas = PersonaList.model_validate_json(file.read())
                    self.state.message += "Research loaded from file."
            except Exception as e:
                print(f"Unable the load personas.json: {e}")
                
    def record_scenarios(self, scenarios: List[Scenario]):
        with open("scenarios.json", "a") as file:
            for scenario in scenarios:
                file.write(scenario.model_dump_json() + "\n")

    @start()
    def ux_research(self):
        if self.state.personas:
            print("Personas exist and skipping UX research")
            self.state.message += " | UX research skipped as it exists"
            return self.state.personas
        # Run the content crew for this section
        result = UserResearchCrew().crew().kickoff()
        self.state.personas = result.pydantic
        self.state.message = "UX research completed first time"
        return self.state.personas

    @listen(ux_research)
    def scenario_development(self, ux_output):
        print("Starting scenario development")

        total_scenarios = 0
        for i, persona in enumerate(ux_output.personas):
            # print("The persona is:" + persona)
            try:
                print(f"{i}: Working on {persona.full_name} scenarios development")
                
                result = ScenarioCrew().crew().kickoff(
                    inputs={
                        "user_persona": persona.model_dump_json() # pydantic way to convert to json string
                    }
                )
                total_scenarios += len(result.pydantic.scenarios)
                self.record_scenarios(result.pydantic.scenarios)
            except ValidationError as e:
                print(f"Validation error in {persona.full_name} and {result.pydantic.scenarios}: {e}")
                continue
            except Exception as e:
                print(f"Error occurred in {persona.full_name}: {e}")
                break

        print(f"Total {total_scenarios} scenarios are generated")
        self.state.message += " | Scenario development completed"
        return "Scenario development completed"



def kickoff():
    ux_flow = UXFlow()
    ux_flow.kickoff()
    # return final_output

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
