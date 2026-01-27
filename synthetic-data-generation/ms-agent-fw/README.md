## Installation

I installed the Microsoft Agent Framework package by following the instruction from [Getting Started](https://github.com/microsoft/agent-framework/blob/main/python/README.md) document. 

For quick summary (installed as in dev mode):

- Installed the Azure CLI - full guide [Web link](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?view=azure-cli-latest&pivots=apt)
```shell
pip install agent-framework --pre
```

- I also installed the Unsloth to verify that if the synthetic dataset I generated with OpenAI's ChatML format works. 
```shell
uv pip install unsloth datasets transformers
```
