import pandas as pd
import numpy as np

def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy().reset_index()
    if "Date" not in df.columns:
        df["Date"] = df.index

    df["Fast_MA"] = df["Close"].rolling(window=20).mean()
    df["Medium_MA"] = df["Close"].rolling(window=50).mean()
    df["Slow_MA"] = df["Close"].rolling(window=200).mean()

    df["BB_middle"] = df["Close"].rolling(window=20).mean()
    df["BB_std"] = df["Close"].rolling(window=20).std()
    df["BB_upper"] = df["BB_middle"] + (2 * df["BB_std"])
    df["BB_lower"] = df["BB_middle"] - (2 * df["BB_std"])

    delta = df["Close"].diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=14).mean()
    avg_loss = pd.Series(loss).rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    df["EMA12"] = df["Close"].ewm(span=12, adjust=False).mean()
    df["EMA26"] = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = df["EMA12"] - df["EMA26"]
    df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()

    return df

def detect_signals(df: pd.DataFrame):
    df = calculate_indicators(df)
    signals = []

    for i in range(1, len(df)):
        if df["Fast_MA"].iloc[i] > df["Medium_MA"].iloc[i] and df["Fast_MA"].iloc[i-1] <= df["Medium_MA"].iloc[i-1]:
            signals.append({"date": df["Date"].iloc[i],"price": df["Close"].iloc[i],"action": "BUY","type": "MA crossover"})
        elif df["Fast_MA"].iloc[i] < df["Medium_MA"].iloc[i] and df["Fast_MA"].iloc[i-1] >= df["Medium_MA"].iloc[i-1]:
            signals.append({"date": df["Date"].iloc[i],"price": df["Close"].iloc[i],"action": "SELL","type": "MA crossover"})

    for i in range(len(df)):
        if df["RSI"].iloc[i] < 30:
            signals.append({"date": df["Date"].iloc[i],"price": df["Close"].iloc[i],"action": "BUY","type": "RSI oversold"})
        elif df["RSI"].iloc[i] > 70:
            signals.append({"date": df["Date"].iloc[i],"price": df["Close"].iloc[i],"action": "SELL","type": "RSI overbought"})

    for i in range(1, len(df)):
        if df["MACD"].iloc[i] > df["MACD_Signal"].iloc[i] and df["MACD"].iloc[i-1] <= df["MACD_Signal"].iloc[i-1]:
            signals.append({"date": df["Date"].iloc[i],"price": df["Close"].iloc[i],"action": "BUY","type": "MACD crossover"})
        elif df["MACD"].iloc[i] < df["MACD_Signal"].iloc[i] and df["MACD"].iloc[i-1] >= df["MACD_Signal"].iloc[i-1]:
            signals.append({"date": df["Date"].iloc[i],"price": df["Close"].iloc[i],"action": "SELL","type": "MACD crossover"})

    return signals
