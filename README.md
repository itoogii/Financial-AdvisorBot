# &#129517; Financial Advisor Bot

&#127891; The project for CM3070

## Project Structure

- [Synthetic Dataset generation](#part-1-multi-turn-conversation-synthetic-data-generation)
  - [User-Persona and Scenario generation using Agentic AI](#section-1-user-persona-creation-plus-conversation-topics-for-each-personas)
  - [Multi-turn conversation dataset generation using Agentic AI](#section-2-conversation-dataset-creation)
- [Model Fine-tuning](#part-2-fine-tuning-small-language-model)
- [Reinforcement Learning](#part-3-reinforcement-learning)
- [FrontEnd Web interface](#part-4-front-end)
- [BackEnd API endpoint](#part-5-back-end)

## Project parts

### Part 1: Multi-turn conversation synthetic data generation

I used the GPT-4.1 model on Azure AI Foundry to generate 147 user personas and plan over 1400 multi-turn conversation scenarios between those personas and a financial expert. Total 40 million tokens used.

```
├── 📂 synthetic-data-generation
│   ├── 📂 crewai            # CrewAI Agentic Synthetic data generation
│   |   ├── 📂 consultgen    # Tested crews to generate synthetic data
│   |   ├── 📂 conv-flow     # Synthetic dataset generation using CrewAI Flows
│   |   ├── 📂 crewai-book   # CrewAI practice notebook
│   ├── 📂 experimentation   # Practice and test scripts and notebook
│   └── 📂 ms-agent-fw       # Synthetic conversation dataset using Microsoft Agent Framework
```

#### Section 1: User persona creation plus conversation topics for each personas

I used CrewAI to create multi-agent task flows that generated 147 individual user personas, each with their own unique scenarios for initiating financial advice conversations.

<div>
  <img src="./assets/Bethany_Morgan.png" alt="Alt text" width="500">
  <p>The generated image is for illustration purpose only (Microsoft Copilot GPT-5.1):</p>
</div>

#### Section 2: Conversation dataset creation

I used the Microsoft Agent Framework (formerly AutoGen) to simulate multi-turn conversations between users seeking financial advice and a professional financial expert.</br>

### Part 2: Fine-tuning small language model

#### Model

&#9940; Llama3 and Gemma3 restricts the engagement in unlicensed financial practice. </br>
&#10071; Phi3.5 and Phi4 had issues with fine-tuning in Unsloth. </br>
&#127752; Owen3 has permissive license, no issues in Unsloth and worked perfectly.

### Part 3: Reinforcement Learning

&#128218; 1. Data Engineering (Collection, Exploration, Preprocessing) </br>
&#128187; 2. Data loading for the state and observations </br>
&#128185; 3. Market Environment creation using Farama's Gymnasium </br>
&#129516; 4. DQN network, DQN-Agent, Replay buffer, DQN-training implementations

### Part 4: Front-End

Web application development using Next.js AI SDK.

### Part 5: Back-end

Simple FastAPI implementation with single API endpoint to utilize the DQN RL model to predict the trend.
