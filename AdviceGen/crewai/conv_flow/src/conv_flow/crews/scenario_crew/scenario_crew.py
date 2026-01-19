from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from dotenv import load_dotenv
import os
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

# Phi3:medium is 4K context window model with 14B parameters
llm_ollama = LLM(model="ollama/phi3:medium", base_url="http://localhost:11434")

load_dotenv()
model = "azure/gpt-5.1-chat"
api_url = os.environ.get("AZURE_API_BASE")
api_key = os.environ.get("AZURE_API_KEY")
api_version = os.environ.get("AZURE_API_VERSION")

llm_azure = LLM(
    model="azure/gpt-5.1-chat",
    endpoint=api_url,
    api_key=api_key,
    api_version=api_version,
)

@CrewBase
class ScenarioCrew():
    """ScenarioCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['scenario_planner'], # type: ignore[index]
            llm=llm_azure,
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['scenario_reviewer'], # type: ignore[index]
            llm=llm_azure,
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def scenario_task(self) -> Task:
        return Task(
            config=self.tasks_config['scenario_task'], # type: ignore[index]
        )

    @task
    def scenario_review_task(self) -> Task:
        return Task(
            config=self.tasks_config['scenario_review_task'], # type: ignore[index]
            output_file='scenarios.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ScenarioCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
