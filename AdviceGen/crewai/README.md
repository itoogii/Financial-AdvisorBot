## CrewAI installation

I followed the installation instruction on [CrewAI Installation](https://docs.crewai.com/en/installation).

### Conversation Generator - ConsultGen
I installed the crewai package to "consultgen", and updated the agents and tasks for the synthetic user persona. 


For quick note:
- First install the crewai tool
```shell
uv tool install crewai
uv tool list
uv tool install crewai --upgrade
```
- Second create crewai project using the CLI
```shell
crewai create crew consultgen
```

### CrewAI in notebook - crewai-book

I installed the CrewAI package using "uv pip" to test in jupyter notebook as shown below:
```shell
uv pip install crewai
```

To use ollama from the CrewAI, I installed [litellm](https://docs.litellm.ai/docs/) as well: 
```shell
uv pip install litellm
```
