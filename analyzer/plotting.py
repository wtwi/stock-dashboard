import os
import time
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHART_DIR = os.path.join(BASE_DIR, "static", "charts")
os.makedirs(CHART_DIR, exist_ok=True)

CHART_TTL = 3600  # 1 hour


def plot_stock_with_signals(df, signals, ticker):
    chart_path = os.path.join(CHART_DIR, f"{ticker}.png")

    # Reuse chart if fresh
    if os.path.exists(chart_path):
        age = time.time() - os.path.getmtime(chart_path)
        if age < CHART_TTL:
            return f"charts/{ticker}.png"

    # Generate new chart
    plt.figure(figsize=(10, 4))
    plt.plot(df["Close"], label="Close")

    for s in signals:
        color = "green" if s["action"] == "BUY" else "red"
        plt.scatter(s["date"], s["price"], color=color)

    plt.title(ticker)
    plt.tight_layout()
    plt.savefig(chart_path)
    plt.close()

    return f"charts/{ticker}.png"
