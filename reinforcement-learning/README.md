## Installation

Python environment in Python 3.14 with required packages from requirements.txt
```shell
#Using pyenv
pyenv virtualenv 3.14 rl-project-3.14
pyenv activate rl-project-3.14
```

## The definition  


To forecast a future trend of the stock prices, I will use a daily historical stock price dataset to train the Reinforcement learning model. 
The dataset must be prepared as "clean" and "transformed". 
Plan for data preparation:
- Find dataset (Free to use dataset, will not re-upload to public data storage due to licensing concerns) / update .gitignore
- Find a simple method to normalize the price data values. The prices range widely, and they differ a lot from one company to another, and the split and merge of the stocks could affect the future prices from $1000 to $10. I need to make them normalized before feeding to ML training. Probably the RSI or MFI indicators are good to get started. 
- Select a window size for dataframe that will be used for each step in ML training and later in the inference. 
- What to predict? 
  - To simplify, the model will estimate whether the stock is worth buying (will go up - bull) or to avoid (will go down - bear) or not sure about (fluctuating). 
- In what extent? 
  - I assume that it is too much noisy and unpredictable when estimating a next day of price trend as anything could happen in that short period. Such as a global or domestic major events, company announcement on a new product, merger etc., However, I believe it is less noisy to predict trend in a month. I could be wrong, but this is how it should be in my development.  

Plan for reinforcement learning:
- Setup with Farama's Gymnasium environment. 
- Use CleanRL or StableBaseline3. Decide which algorithm to use to train the RL. 
- Define the environment rule - when to end the episode, what would be the reward, action. State will be the 
- Build and train the RL model
- Evaluate the performance of the model 
Reward function:
- The estimates are: Rise, Fall, Neutral
- Reward of +0 going to state 
- Reward of +1 going to state
- Reward of -1 going to state 

**Note**  
The Monte-Carlo seems not suitable. In my opinion, it should experience different price movements everytime where it shouldn't have any prior episodic interactions to update the value function. 