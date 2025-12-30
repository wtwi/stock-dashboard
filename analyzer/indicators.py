import numpy as np
import pandas as pd

def add_moving_averages(df: pd.DataFrame, fast: int, medium: int, slow: int) -> pd.DataFrame:
    df["Fast_MA"] = df["Close"].rolling(fast).mean()
    df["Medium_MA"] = df["Close"].rolling(medium).mean()
    df["Slow_MA"] = df["Close"].rolling(slow).mean()
    return df

def add_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    delta = df["Close"].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.ewm(com=period-1, adjust=False).mean()
    avg_loss = loss.ewm(com=period-1, adjust=False).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    df["RSI"] = 100 - (100 / (1 + rs))
    return df

def add_bollinger_bands(df: pd.DataFrame, period: int = 20, num_std: float = 2.0) -> pd.DataFrame:
    ma = df["Close"].rolling(period).mean()
    std = df["Close"].rolling(period).std()
    df["Bollinger_Mid"] = ma
    df["Bollinger_Upper"] = ma + num_std * std
    df["Bollinger_Lower"] = ma - num_std * std
    return df

def add_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    ema_fast = df["Close"].ewm(span=fast, adjust=False).mean()
    ema_slow = df["Close"].ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    df["MACD"] = macd_line
    df["MACD_Signal"] = signal_line
    df["MACD_Hist"] = macd_line - signal_line
    return df

def add_atr(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    high = df["High"]
    low = df["Low"]
    close = df["Close"]

    prev_close = close.shift(1)
    tr = pd.concat([
        (high - low),
        (high - prev_close).abs(),
        (low - prev_close).abs()
    ], axis=1).max(axis=1)

    df["ATR"] = tr.rolling(period).mean()
    return df

def add_volume_ma(df: pd.DataFrame, period: int = 20) -> pd.DataFrame:
    if "Volume" in df.columns:
        df["Volume_MA"] = df["Volume"].rolling(period).mean()
    return df


# ---------------------------------------------------------
# NEW: The orchestrator function main.py expects
# ---------------------------------------------------------

def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Ensure Date column exists
    if "Date" not in df.columns:
        df["Date"] = df.index

    # Ensure OHLC columns are 1D floats
    for col in ["Open", "High", "Low", "Close"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Apply all indicator helpers
    df = add_moving_averages(df, fast=20, medium=50, slow=200)
    df = add_bollinger_bands(df, period=20, num_std=2.0)
    df = add_rsi(df, period=14)
    df = add_macd(df, fast=12, slow=26, signal=9)
    df = add_atr(df, period=14)
    df = add_volume_ma(df, period=20)

    return df
