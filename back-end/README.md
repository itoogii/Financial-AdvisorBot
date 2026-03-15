# Backend service

This is an application to provide the service for the price estimation. This service will run on FastAPI and expose endpoint for the trend prediction.

## Installation

### Python environment

```shell
uv venv -p 3.14 ~/pythonenvs/advisorbot-backend-3.14
source ~/pythonenvs/advisorbot-backend-3.14/bin/activate
```

### Requirements

```shell
uv pip install -r requirements.txt
```

## Running

```shell
fastapi dev
```

## App service

The app uses yfinance module to retrieve the recent price data and estimates the stock trend using DQN model.
