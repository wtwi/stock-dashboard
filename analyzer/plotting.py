import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import datetime

def plot_stock_with_signals(df, signals, ticker):
    # Filter to last 2 years
    two_years_ago = datetime.datetime.now() - datetime.timedelta(days=730)
    df = df[df["Date"] >= two_years_ago]

    # Apply black theme
    plt.style.use("dark_background")

    fig, ax = plt.subplots(figsize=(10, 4))

    # Plot price and Bollinger Bands
    line_close, = ax.plot(df["Date"], df["Close"], label="Close", color="cyan", linewidth=1.2)
    line_mid,   = ax.plot(df["Date"], df["Bollinger_Mid"], label="BB Mid", color="orange", linewidth=1)
    line_up,    = ax.plot(df["Date"], df["Bollinger_Upper"], label="BB Upper", color="red", linestyle="--", linewidth=0.8)
    line_low,   = ax.plot(df["Date"], df["Bollinger_Lower"], label="BB Lower", color="green", linestyle="--", linewidth=0.8)

    # Plot signals WITHOUT labels (so they don't appear in legend)
    for signal in signals:
        if signal["date"] >= two_years_ago:
            color = "lime" if signal["action"] == "BUY" else "magenta"
            ax.scatter(signal["date"], signal["price"], color=color, s=40, marker="o")

    # Format x-axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    fig.autofmt_xdate()

    ax.set_title(ticker)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.grid(True, linestyle="--", alpha=0.3)

    # Legend ONLY for lines
    ax.legend(
        handles=[line_close, line_mid, line_up, line_low],
        loc="upper left",
        fontsize=8
    )

    # Save chart
    chart_dir = os.path.join("static", "charts")
    os.makedirs(chart_dir, exist_ok=True)
    chart_path = os.path.join(chart_dir, f"{ticker}.png")
    plt.savefig(chart_path, bbox_inches="tight")
    plt.close()

    return chart_path
