import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from analyzer.tickers import TICKER_NAMES

plt.style.use("dark_background")

def plot_stock_with_signals(df, signals, ticker: str):
    df = df.reset_index()
    if "Date" not in df.columns:
        df["Date"] = df.index
    df["Date"] = pd.to_datetime(df["Date"])

    # --- Bollinger Bands (20 MA ± 2 std) ---
    if "Close" in df.columns:
        df["BB_MA"] = df["Close"].rolling(window=20).mean()
        df["BB_Upper"] = df["BB_MA"] + 2 * df["Close"].rolling(window=20).std()
        df["BB_Lower"] = df["BB_MA"] - 2 * df["Close"].rolling(window=20).std()

    fig, (ax_price, ax_vol, ax_ind) = plt.subplots(
        3, 1, figsize=(12,10), sharex=True,
        gridspec_kw={'height_ratios':[3,1,1]}
    )

    # --- PRICE + MOVING AVERAGES ---
    ax_price.plot(df["Date"], df["Close"], label="Close", color="white", linewidth=1.5)
    for col, color, label in [
        ("Fast_MA", "blue", "20 MA"),
        ("Medium_MA", "orange", "50 MA"),
        ("Slow_MA", "red", "200 MA")
    ]:
        if col in df.columns:
            ax_price.plot(df["Date"], df[col].fillna(method="bfill"), label=label, color=color, linewidth=1.2)

    # Bollinger Bands + shaded channel
    if "BB_Upper" in df.columns and "BB_Lower" in df.columns:
        ax_price.plot(df["Date"], df["BB_Upper"], label="Bollinger Upper", color="green", linestyle="--", linewidth=1.0)
        ax_price.plot(df["Date"], df["BB_Lower"], label="Bollinger Lower", color="red", linestyle="--", linewidth=1.0)
        ax_price.fill_between(df["Date"], df["BB_Lower"], df["BB_Upper"],
                              color="grey", alpha=0.2, label="Bollinger Band")

    # BUY/SELL arrows
    seen_dates = set()
    for s in signals[::-1]:
        if len(seen_dates) >= 5:
            break
        if s["date"] in seen_dates:
            continue
        seen_dates.add(s["date"])
        if s["action"] == "BUY":
            ax_price.scatter(s["date"], s["price"], marker="^", color="lime", s=120,
                             edgecolors="black", linewidths=1.0, zorder=5)
        elif s["action"] == "SELL":
            ax_price.scatter(s["date"], s["price"], marker="v", color="red", s=120,
                             edgecolors="black", linewidths=1.0, zorder=5)

    # Title
    company_name = TICKER_NAMES.get(ticker, ticker)
    ax_price.set_title(f"{company_name} — Price + MA + Bollinger + Support", color="cyan")

    # Support/Resistance line
    recent = df.tail(60)
    if not recent.empty:
        min_idx = recent["Close"].idxmin()
        max_idx = recent["Close"].idxmax()
        ax_price.plot([df.loc[min_idx,"Date"], df.loc[max_idx,"Date"]],
                      [df.loc[min_idx,"Close"], df.loc[max_idx,"Close"]],
                      color="lime", linestyle="--", linewidth=1.5, label="Support/Resistance")

    ax_price.legend(loc="best")
    ax_price.grid(True, alpha=0.3)

    # --- VOLUME ---
    if "Volume" in df.columns:
        ax_vol.bar(df["Date"], df["Volume"], color="grey", alpha=0.6)
        ax_vol.set_ylabel("Volume")
        ax_vol.grid(True, alpha=0.3)

    # --- RSI + MACD ---
    if "RSI" in df.columns:
        ax_ind.plot(df["Date"], df["RSI"].fillna(method="bfill"), label="RSI", color="purple", linewidth=1.2)
        ax_ind.axhline(70, color="red", linestyle="--", alpha=0.5)
        ax_ind.axhline(30, color="green", linestyle="--", alpha=0.5)
    if "MACD" in df.columns and "MACD_Signal" in df.columns:
        ax_ind.plot(df["Date"], df["MACD"].fillna(method="bfill"), label="MACD", color="cyan", linewidth=1.2)
        ax_ind.plot(df["Date"], df["MACD_Signal"].fillna(method="bfill"), label="Signal", color="magenta", linewidth=1.2)

    ax_ind.set_ylabel("Indicators")
    handles, labels = ax_ind.get_legend_handles_labels()
    if labels:
        ax_ind.legend(loc="best")
    ax_ind.grid(True, alpha=0.3)

    # --- Date formatting ---
    ax_price.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    fig.autofmt_xdate()

    # --- SAVE CHART ---
    plt.tight_layout()
    os.makedirs("static", exist_ok=True)
    filename = f"static/{ticker}_chart.png"
    plt.savefig(filename, facecolor="black", dpi=120)
    plt.close()
    return filename
