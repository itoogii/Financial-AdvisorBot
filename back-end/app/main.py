from fastapi import FastAPI
import os

from .services.dqn import QNetwork
from .services.dataloader import data_collector, data_preprocessing
import torch

model_path = os.path.join(os.path.dirname(__file__), "dqn_model.pth")

device = torch.device(torch.accelerator.current_accelerator() if torch.accelerator.is_available() else "cpu")

app = FastAPI()

q_network = QNetwork().to(device)
q_network.load_state_dict(torch.load(model_path))


@app.get("/estimate/{ticker}")
async def get_estimate(ticker: str):

    df = data_collector(ticker)
    observation = data_preprocessing(df)
    if observation is None:
        return {"tool_response": f"Unfortunately, there is not enough data available for the ticker {ticker}. Unable to estimate the trend!"}
    with torch.no_grad():
        # since now I am using np.float32(60, 5) shape observation, I need to change it to torch.tensor(1, 60, 5) shape before passing to the network
        observation = torch.tensor(observation, dtype=torch.float32).to(device)
        q_values = q_network(observation)
        action_index = int(torch.argmax(q_values, dim=1).item())
    
    action = ["hold", "buy", "sell"][action_index]
    return {"tool_response": f"The DQN Agent estimates that the trend for {ticker} is: {action}. Please remind the user that the estimate can be wrong!"}