<<<<<<< HEAD
from analyzer.config import STOCK_TICKERS, FAST_MA, MEDIUM_MA, SLOW_MA, RSI_PERIOD
from analyzer.data import get_stock_data
from analyzer.indicators import add_moving_averages, add_rsi
from analyzer.signals import detect_signals

print("Running stock analyzer...\n")

for ticker in STOCK_TICKERS:
    print(f"Checking {ticker}...")

    df = get_stock_data(ticker)
    if df is None:
        print(f"  No data for {ticker}")
        continue

    df = add_moving_averages(df, FAST_MA, MEDIUM_MA, SLOW_MA)
    df = add_rsi(df, RSI_PERIOD)

    signals = detect_signals(df)

    if not signals:
        print("  No signals.")
    else:
        for action, sig_type, date, price in signals[-3:]:
            print(f"  {action} | {sig_type} | {date.date()} | ${price:.2f}")

print("\nDone.")
=======
from analyzer.config import STOCK_TICKERS, FAST_MA, MEDIUM_MA, SLOW_MA, RSI_PERIOD
from analyzer.data import get_stock_data
from analyzer.indicators import add_moving_averages, add_rsi
from analyzer.signals import detect_signals

print("Running stock analyzer...\n")

for ticker in STOCK_TICKERS:
    print(f"Checking {ticker}...")

    df = get_stock_data(ticker)
    if df is None:
        print(f"  No data for {ticker}")
        continue

    df = add_moving_averages(df, FAST_MA, MEDIUM_MA, SLOW_MA)
    df = add_rsi(df, RSI_PERIOD)

    signals = detect_signals(df)

    if not signals:
        print("  No signals.")
    else:
        for action, sig_type, date, price in signals[-3:]:
            print(f"  {action} | {sig_type} | {date.date()} | ${price:.2f}")

print("\nDone.")
>>>>>>> 28c2ef6ef5529dccf4d660e68dbd01b5e0aa2e3d
