import pandas as pd



# To read historical stock data from yfinance Ticker object
def data_collector(ticker: str) -> pd.DataFrame:
    import yfinance as yf
    from datetime import date
    import datetime as dt
    today = date.today()
    past = dt.timedelta(days=200)
    start_date = today - past
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(
            start=start_date, 
            interval="1d", 
            prepost=False, 
            auto_adjust = False)
        return history
    except Exception as e:
        print(f"An error occurred while loading history: {e}")
        return pd.DataFrame()


def data_preprocessing(df: pd.DataFrame) -> pd.DataFrame:
    import numpy as np
    import ta
    df = df.copy()
    window = 26
    if df.empty:
        return None
    if hasattr(df.index, 'tz') and df.index.tz is not None:
        df.index = df.index.tz_localize(None)

    df = df[['Open', 'High', 'Low', 'Close', 'Adj Close','Volume']]
    # skip all rows with missing values
    df = df.dropna(axis=0)

    # Step 1: Check for duplicates
    duplicate_rows = df.duplicated().sum()
    if duplicate_rows > 0:
        df = df.drop_duplicates()

    # Step 2: Check for integrity
    if (df[['Open', 'High', 'Low', 'Close', 'Volume']] <= 0).any().any():
        # only return the rows with positive prices
        valid_rows = (df[['Open', 'High', 'Low', 'Close', 'Volume']] > 0).all(axis=1)
        df = df[valid_rows]
    if (df['High'] < df['Low']).any():
        # only return the rows with High >= Low
        valid_rows = (df['High'] >= df['Low'])
        df = df[valid_rows]

    # Step 3: Calculate MACD
    macd =ta.trend.MACD(close=df['Close'], window_slow= 26, window_fast= 12, window_sign = 9, fillna = False) 
    df['MACD_line'] =macd.macd()
    df['MACD_signal'] =macd.macd_signal()
    df['MACD_diff'] =macd.macd_diff()

    # Step 4: Calculate RSI
    df['RSI']=ta.momentum.RSIIndicator(close= df['Close'], window= 14, fillna= False).rsi()

    # Step 5: Normalize the RSI, MACD, and Volume features
    #### RSI ####
    df['RSI_norm'] = (df['RSI'] - 50) / 50.0
    #### MACD ####
    mean_line = df['MACD_line'].rolling(window=window).mean()
    std_line = df['MACD_line'].rolling(window=window).std()
    mean_signal = df['MACD_signal'].rolling(window=window).mean()
    std_signal = df['MACD_signal'].rolling(window=window).std()
    mean_diff = df['MACD_diff'].rolling(window=window).mean()
    std_diff = df['MACD_diff'].rolling(window=window).std()
    df['MACD_line_norm'] = (df['MACD_line'] - mean_line) / (std_line + 1e-8) # adding epsilon to avoid division error
    df['MACD_signal_norm'] = (df['MACD_signal'] - mean_signal) / (std_signal + 1e-8)
    df['MACD_diff_norm'] = (df['MACD_diff'] - mean_diff) / (std_diff + 1e-8)
    #### Volume ####
    log_volume = np.log1p(df['Volume']) # Because volume ranges widely, using log() to manage the exponential growth. log1p is used to avoid log(0) issue.
    mean = log_volume.rolling(window=window).mean()
    std = log_volume.rolling(window=window).std()
    df['Volume_norm'] = (log_volume - mean) / (std + 1e-8)
    # Adding the previous close price as a feature
    df['Prev_close'] = df['Close'].shift(1)
    # Step 7: Drop null value rows. The MACD, RSI ta calculations created many NaN value rows. Especially, the window size is as big as 260, I had to drop more than 1-year of data. 
    df = df.dropna(axis=0)
    # Step 8: Calculate log returns for the 'Close' price
    # There were 2 issues. 
    # 1. The .shift(1) created the first row with Prev_close as NaN. Solved in Step 6 by dropping null value rows.
    # 2. The log(0) issue. To avoid it, I am using .clip(lower=1e-8) method. 
    df['Return'] = np.log(df['Close'].clip(lower=1e-8)) - np.log(df['Prev_close'].clip(lower=1e-8))
    # Step 9: Drop unnecessary columns
    df = df.drop(columns=['Open', 'Close', 'High', 'Low', 'Adj Close', 'Prev_close', 'MACD_line', 'MACD_signal', 'MACD_diff', 'RSI', 'Volume'])
    
    # Step 10: 
    features = ['RSI_norm', 'MACD_line_norm', 'MACD_signal_norm', 'Volume_norm', 'Return']

    if len(df) < 60: # minimum 60 days of data
        return None
    # returns the shape of (1, 60, 5)
    return np.expand_dims(df[features].iloc[-60:].values, axis=0)

