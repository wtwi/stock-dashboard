import pandas as pd

def detect_signals(df: pd.DataFrame):
    signals = []

    # MA crossover signals
    for i in range(1, len(df)):
        if (
            df["Fast_MA"].iloc[i] > df["Medium_MA"].iloc[i] and
            df["Fast_MA"].iloc[i - 1] <= df["Medium_MA"].iloc[i - 1]
        ):
            signals.append({
                "date": df["Date"].iloc[i],
                "price": df["Close"].iloc[i],
                "action": "BUY",
                "type": "MA crossover"
            })

        elif (
            df["Fast_MA"].iloc[i] < df["Medium_MA"].iloc[i] and
            df["Fast_MA"].iloc[i - 1] >= df["Medium_MA"].iloc[i - 1]
        ):
            signals.append({
                "date": df["Date"].iloc[i],
                "price": df["Close"].iloc[i],
                "action": "SELL",
                "type": "MA crossover"
            })

    # RSI signals
    for i in range(len(df)):
        if df["RSI"].iloc[i] < 30:
            signals.append({
                "date": df["Date"].iloc[i],
                "price": df["Close"].iloc[i],
                "action": "BUY",
                "type": "RSI oversold"
            })
        elif df["RSI"].iloc[i] > 70:
            signals.append({
                "date": df["Date"].iloc[i],
                "price": df["Close"].iloc[i],
                "action": "SELL",
                "type": "RSI overbought"
            })

    # MACD signals
    for i in range(1, len(df)):
        if (
            df["MACD"].iloc[i] > df["MACD_Signal"].iloc[i] and
            df["MACD"].iloc[i - 1] <= df["MACD_Signal"].iloc[i - 1]
        ):
            signals.append({
                "date": df["Date"].iloc[i],
                "price": df["Close"].iloc[i],
                "action": "BUY",
                "type": "MACD crossover"
            })

        elif (
            df["MACD"].iloc[i] < df["MACD_Signal"].iloc[i] and
            df["MACD"].iloc[i - 1] >= df["MACD_Signal"].iloc[i - 1]
        ):
            signals.append({
                "date": df["Date"].iloc[i],
                "price": df["Close"].iloc[i],
                "action": "SELL",
                "type": "MACD crossover"
            })

    return signals
