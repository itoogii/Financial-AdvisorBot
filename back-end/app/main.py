from fastapi import FastAPI

app = FastAPI()


@app.get("/estimate/{ticker}")
async def get_estimate(ticker: str):
    
    return {"ticker": ticker}