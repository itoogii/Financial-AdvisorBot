
## Installation

Python environment setup using pyenv:
```shell
#Using pyenv
pyenv virtualenv 3.14 rl-project-3.14
pyenv activate rl-project-3.14
pip install -r requirements.txt
```

## The definition  

To forecast a future trend of the stock prices, I used a daily historical stock price dataset to train the Reinforcement learning model. 
The historical stock price dataset was sourced from Kaggle. However, as that data ends in April 2020, I downloaded recent market data from Yahoo Finance (using the yfinance library) to cover the period through February 2026. I removed 1944 changed or delisted tickers from the final training and test datasets (in parquet format) to ensure consistency.

### The custom Gym environment
The Farama Gymnasium documentation provides the following key design questions for the custom environment design.  
📚 **What skill should the agent learn?**  
-Predict the stock trend (up, down, flat)

&#x1F50E; **What information does the agent need?**  
-Agent needs today's technical analysis indicators for a given stock as an observation.  

&#x1F3F9; **What actions can the agent take?**  
-Discrete choices (up trend - bullish, down trend - bearish, sideways - neutral).   

&#x1F3C6; **How do we measure success?**
-I measure the success by rewards it received from the accurate predictions

&#x1F31C; **When should episodes end?**
-An episode ends once all available historical data for a given stock has been processed.
-Episodes (Epoch) end after all data in the training dataset has been processed.  




- Find a simple method to normalize the price data values. The prices range widely, and they differ a lot from one company to another, and the split and merge of the stocks could affect the future prices from $1000 to $10. I need to make them normalized before feeding to ML training. Probably the RSI or MFI indicators are good to get started. 
- Select a window size for dataframe that will be used for each step in ML training and later in the inference. 
- What to predict? 
  - To simplify, the model will estimate whether the stock is worth buying (will go up - bull) or to avoid (will go down - bear) or not sure about (fluctuating). 
- In what extent? 
  - I assume that it is too much noisy and unpredictable when estimating a next day of price trend as anything could happen in that short period. Such as a global or domestic major events, company announcement on a new product, merger etc., However, I believe it is less noisy to predict trend in a month. I could be wrong, but this is how it should be in my development.  



## Compliance & Data Usage
This project utilizes financial market data for educational and research purposes. To ensure compliance with data provider terms and licensing, please note the following:

Data Sources: Data was sourced via the yfinance library and historical archives from Kaggle (which are derivatives of Yahoo Finance data).

Non-Redistribution: To comply with terms of service and licensing, no raw data files (CSV/Parquet) are included in this repository.

Permitted Use: This project is strictly non-commercial. The analysis and models developed here are intended for personal learning and academic demonstration.