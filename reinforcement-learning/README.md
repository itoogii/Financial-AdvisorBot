# Reinforcement Learning

The reinforcement learning is developed in stages of testing and exploring data source, collecting data, evaluating dataset, feature selection, data preprocessing, processing data for RL training, development of Reinforcement learning in DQN architecture and training the DQN model.

## &#9996; Setup

Python environment setup using pyenv:

```shell
#Using pyenv
pyenv virtualenv 3.14 rl-project-3.14
pyenv activate rl-project-3.14
pip install -r requirements.txt
```

Python environment setup using uv:

```shell
uv venv -p 3.14 ~/pythonenvs/advisorbot-rl-3.14
source ~/pythonenvs/advisorbot-rl-3.14/bin/activate
uv pip install -r requirements.txt
```

## &#9997; The definition

To forecast a future trend of the stock prices, I used a daily historical stock price dataset to train the Reinforcement learning model.
The historical stock price dataset was sourced from Kaggle. Additionally, as that data ends in April 2020, I downloaded new market data from Yahoo Finance (using the yfinance library) to cover the period until February 2026. I removed 1944 changed or delisted tickers from the final training and test datasets (in parquet format) to ensure consistency.

## &#127757; The custom Gym environment

Key questions for the custom environment (source: The Farama Gymnasium documentation) helped me picture the design for the environment. </br>

🍋 **What skill should the agent learn?**  
-Predict the stock trend (up, down, flat)

&#x1F34B; **What information does the agent need?**  
-Agent needs today's technical analysis indicators for a given stock as an observation.

&#x1F34B; **What actions can the agent take?**  
-Discrete choices (up trend - bullish or buy, down trend - bearish or sell, sideways - neutral or hold).

&#x1F34B; **How do we measure success?**  
-I measure the success by rewards it received from the accurate predictions

&#x1F34B; **When should episodes end?**

- A single episode is full cycle of processing a stock historical data.
- Epoch is full cycle of processing all available training data.
- Training will terminate when it hits the minimum reward value.

## Data Usage

To comply with the yfinance terms and licensing, the stock market data is used for educational and research purposes, and no raw data files (CSV/Parquet) are included in this repository.
This project is strictly non-commercial. The analysis and models developed here are intended for academic purposes.
