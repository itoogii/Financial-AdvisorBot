from fastapi import FastAPI
from pathlib import Path

from .services.dqn import QNetwork
from .services.dataloader import data_collector, data_preprocessing
import torch


model_path = Path(__file__).parent / "rlmodel" / "rl_dqn.pth"

device = torch.device(torch.accelerator.current_accelerator() if torch.accelerator.is_available() else "cpu")

app = FastAPI()

q_network = QNetwork().to(device)
q_network.load_state_dict(torch.load(model_path))


@app.get("/estimate/{ticker}")
async def get_estimate(ticker: str):

    df = data_collector(ticker)
    observation = data_preprocessing(df)
    if observation is None:
        return {"response": f"There is not enough data available for the ticker {ticker}. Unable to estimate the trend."}
    with torch.no_grad():
        # since now I am using np.float32(60, 5) shape observation, I need to change it to torch.tensor(1, 60, 5) shape before passing to the network
        observation = torch.tensor(observation, dtype=torch.float32).to(device)
        q_values = q_network(observation)
        action_index = int(torch.argmax(q_values, dim=1).item())
    action = [{"signal": "Hold", "message": "No significant price movement is predicted" }, 
              {"signal": "Buy", "message": "Bullish trend detected and consider buying as the trend is positive" }, 
              {"signal": "Sell", "message": "Bearish trend detected and consider selling as the trend is negative" }][action_index]
    print("Estimated action index:", action_index, f"The DQN Agent estimates that the trend for {ticker} is: {action}.")
    return {"response": f"The agent predicted {action["signal"]} signal for the {ticker}. {action["message"]}. Remind user of the investment risks associated with this prediction."}


@app.get("/last_price/{ticker}")
async def get_last_price(ticker: str):

    df = data_collector(ticker)
    last_close_price = df['Close'].iloc[-1] if not df.empty else None
    
    if last_close_price is None:
        return {"response": f"There is not enough data available for the ticker {ticker}. Unable to get the last price."}
    print(f"The last close price for {ticker} is ${last_close_price:.2f}.")
    return {"response": f"The last close price for {ticker} is ${last_close_price:.2f}."}
   