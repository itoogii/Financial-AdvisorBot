## Synthetic data generation with CrewAI


## Directory structure
- crewai: CrewAI Agentic Synthetic data generation
    * consultgen: The CrewAI crews test to generate synthetic data. 
    * conv-flow: The CrewAI Flows to control the synthetic data generation 
    * crewai-book: The jupyter notebooks to evaluate the CrewAI. 

## CrewAI installation

I followed an installation instruction from [CrewAI Installation](https://docs.crewai.com/en/installation).  

For **quick reference**, I did following to create CrewAI Crews project:
- First installed the crewai tool
```shell
uv tool install crewai
uv tool list
uv tool install crewai --upgrade
```
- Second created crewai project using the CLI
```shell
crewai create crew consultgen
```
For **quick reference**, I did following to create CrewAI Flows project: 
```shell
crewai create flow conv-flow
```

### ConsultGen
In my early User Persona generation, I installed crewai package in "consultgen" directory, and updated the agents and tasks for the synthetic user persona generation. 
The report from the User Persona is renamed to "generated_personas.md". 


### Conv_flow
https://docs.crewai.com/en/guides/flows/first-flow

### CrewAI in notebook - crewai-book

I installed the CrewAI package using "uv pip" to test in jupyter notebook as shown below:
```shell
uv pip install crewai
```

To use ollama from the CrewAI, I installed [litellm](https://docs.litellm.ai/docs/) as well: 
```shell
uv pip install litellm
```
