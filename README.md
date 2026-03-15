# &#129517; Financial Advisor Bot

&#127891; The project for CM3070

## Project Structure

- [Synthetic Dataset generation](#part-1-multi-turn-conversation-synthetic-data-generation)
  - [User-Persona and Scenario generation using Agentic AI](#section-1-user-persona-creation-plus-conversation-topics-for-each-personas)
  - [Multi-turn conversation dataset generation using Agentic AI](#section-2-conversation-dataset-creation)
- [Model Fine-tuning](#part-2-fine-tuning-small-language-model)
- [Reinforcement Learning](#part-3-reinforcement-learning)
- [FrontEnd Web interface](#part-4-front-end)
- [BackEnd API](#part-5-back-end)

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

#### Model selection

&#128683; Llama3 and Gemma3 restricts the engagement in unlicensed financial practice. </br>
&#128680; Phi3.5 and Phi4 had issues with fine-tuning in Unsloth. </br>
&#127752; Owen3 has permissive license, no issues in Unsloth and worked perfectly.

#### Model fine-tuning

I fine-tuned the Qwen3-4B model with my multi-turn conversation dataset using Unsloth. The model is then uploaded to Huggingface.

### Part 3: Reinforcement Learning

The reinforcement learning is implemented in following steps.
&#128218; 1. Data Engineering (Collection, Exploration, Preprocessing) </br>
&#128187; 2. Data loading and processing (environment state/observations data) </br>
&#128185; 3. Custom Market Environment creation with Farama's Gymnasium </br>
&#129516; 4. DQN network, DQN-Agent, Replay buffer, DQN-training implementations

### Part 4: Back-end

Simple FastAPI implementation with two API endpoints to utilize the DQN RL model and yfinance to predict the trend.

### Part 5: Front-End

Web application development using Next.js AI SDK, AI Elements by adapting the Vercel Chatbot template.

## Deployment

This project is aimed at deploying on a local system.

Here are the steps to run.

### Backend service: </br>

```bash
$ source ~/pythonenvs/advisorbot-backend-3.14/bin/activate
$ cd back-end
$ fastapi dev
```

### Language model: </br>

The fine-tuned model is uploaded to Huggingface model repository. [Click to download the model &#9875;](https://huggingface.co/Battogtokh/Qwen3-4B-Instruct-unsloth-FinAdvisor-gguf).

I installed ollama on my local machine, and created the model using the ./Modelfile (please make sure the model name is the same in FROM field if downloaded).

```bash
$ cd fine-tuning
$ ollama create qwen3-unsloth-finadvisor -f ./Modelfile
```

(&#128735; Not necessary) To run the model explictly:

```bash
$ ollama run qwen3-unsloth-finadvisor:latest
```

&#9977; Note that it wasn't necessary to run the model as ollama service on my WSL can run it all by itself on calls from the AI SDK or API calls to http://localhost:11434/api/chat. The ollama service is always active and listening on my local machine. Ollama releases system resources after timeout.

### Frontend service: </br>

Please note that the internal tools (under /chatbot/lib/ai/tools) are using "localhost" address to connect to the backend service endpoints.
I could have implemented the .env variable to update the addresses. But my intention is to run on my local machine and it is out of the scope for now.

```bash
$ nvm install 24.14.0
$ nvm use v24.14.0
$ npm install -g pnpm
$ cd front-end/chatbot
$ pnpm install
$ pnpm exec drizzle-kit generate
$ pnpm exec drizzle-kit migrate
$ pnpm run dev
```

&#128679; **Optional** The app safely fails without redis. I used docker to run the redis:

```bash
docker run --name fin-redis -d -v $(pwd)/redis-storage:/data redis:8-alpine redis-server --save 60 1 --loglevel warning
```
