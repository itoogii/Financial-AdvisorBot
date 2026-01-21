# Synthetic dataset generation

In this CrewAI Flows project I added 2 crews to work to generate the user personas and conversation scenarios. 
Each crew has two members. The first crew will generate the user personas in given Pydantic model, and using these user personas the second crew will generate the conversation scenarios with financial advisor. 

## Synthetic files

My crews generated the personas.json file for user personas, and scenarios.json file for conversation scenarios for the personas. Both files are located in this base project directory.
I also tasked the first crew to save the user research document in "research_investor.md". I hope you will find them useful. 


**See Below for CrewAI Instruction** &#x1F447; (provided by CrewAI template)

## Installation

Ensure you have Python >=3.10 <3.14 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:
```bash
crewai install
```

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/conv_flow/config/agents.yaml` to define your agents
- Modify `src/conv_flow/config/tasks.yaml` to define your tasks
- Modify `src/conv_flow/crew.py` to add your own logic, tools and specific args
- Modify `src/conv_flow/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your flow and begin execution, run this from the root folder of your project:

```bash
crewai run
```

This command initializes the conv-flow Flow as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The conv-flow Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the {{crew_name}} Crew or crewAI.

- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
