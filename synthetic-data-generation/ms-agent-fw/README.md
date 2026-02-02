## Installation

I installed the Microsoft Agent Framework package by following the instruction from [Getting Started](https://github.com/microsoft/agent-framework/blob/main/python/README.md) document. 

For quick summary (installed as in dev mode):

- Installed the Azure CLI - full guide [Web link](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?view=azure-cli-latest&pivots=apt)
```shell
pip install agent-framework --pre
```

- I also installed the Unsloth to verify that if the synthetic dataset I generated with OpenAI's ChatML format works. 
```shell
uv pip install unsloth datasets transformers torch
```
## About
The dialogue-dataset.jsonl is formatted in OpenAI ChatML. Refer to Unsloth Dataset guide [Link](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/datasets-guide)  

- The "dialogue-gen.py" is the main script used for generating the synthetic dataset.
- The "financial-expert-dataset.py" is early test version script that I used for local Ollama model. 
- The "chat-simulator.py" is adapted from Microsoft Agent Framework tutorial examples to test the multi-turn group conversation workflow.
- The "simple.py" script is copied from Microsoft Agent Framework (MAF) to test the Azure CLI authentication and Azure AI API with MAF. 
- The "user_lookup.py" script is to find an user persona index inside the "scenarios.json" file. Every time, when I spotted a mistake or hallucinations from the output text, I had to stop the dialogue-gen.py script to correct the agent instructions. To continue the dialogue generation from the user that I interrupted, I also need to know its index position inside the scenarios.json. This script is created to simplify the lookup process. 