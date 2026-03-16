# Microsoft Agent Framework

## &#9996; Setup

I installed the Microsoft Agent Framework (MAF) package by following the instruction from [Getting Started](https://github.com/microsoft/agent-framework/blob/main/python/README.md) document.

For quick summary (installed as in dev mode):

- Installed the Azure CLI - full guide [Web link](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-linux?view=azure-cli-latest&pivots=apt)

```shell
pip install agent-framework --pre
```

- I also installed the Unsloth to verify that if the synthetic dataset I generated with OpenAI's ChatML format works.

```shell
uv pip install unsloth datasets transformers torch
```

## &#9997; About

The dialogue-dataset.jsonl is formatted in OpenAI ChatML. Refer to Unsloth Dataset guide [Link](https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/datasets-guide)

```
├── 📄 dialogue-dataset.jsonl   # Synthetic conversational dataset
├── 📄 dialogue-gen.py          # The script used for generating the synthetic dataset
├── 📂 experiments              #
│   |   ├── 📄 chat-simulator.py                # MAF practice - multi-turn group conversation workflow
│   |   ├── 📄 dataset-evaluation.ipynb         # Quick data evaluation with Unsloth
│   |   ├── 📄 financial-expert-dataset.py      # Test script - I used for local Ollama model
│   |   ├── 📄 simple.py                        # Adapted from MAF to test Azure CLI auth and Azure AI API
└── 📄 user_lookup.py           # Helper script to lookup "persona" index in "scenarios.json"
```

<blockquote>The "user_lookup.py": When hallucinations or errors occur in the output, I have to terminate dialogue-gen.py to update the agent's instructions. To resume generation from the exact point of interruption, I need the specific index of the scenario within scenarios.json. </blockquote>
