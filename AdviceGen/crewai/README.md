## CrewAI installation

I followed the installation instruction on [CrewAI Installation](https://docs.crewai.com/en/installation).
  
For quick note:
```shell
uv tool install crewai
uv tool list
uv tool install crewai --upgrade
```

By following the installation instruction, it creates a template for the chosen provider.  
Instead I installed the CrewAI package, to test in jupyter notebook as shown below:
```shell
uv pip install crewai
```

To use ollama from the CrewAI, I installed [litellm](https://docs.litellm.ai/docs/) as well: 
```shell
uv pip install litellm
```
