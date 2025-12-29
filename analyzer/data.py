import pandas as pd
import yfinance as yf
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

def get_stock_data(ticker: str, period: str = "2y") -> pd.DataFrame | None:
    try:
        df = yf.download(ticker, period=period)
        if df is None or df.empty:
            return None

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join([c for c in col if c]).strip() for col in df.columns.values]

        df = df.reset_index()

        rename_map = {}
        for col in df.columns:
            if "close" in col.lower(): rename_map[col] = "Close"
            elif "volume" in col.lower(): rename_map[col] = "Volume"
            elif "open" in col.lower(): rename_map[col] = "Open"
            elif "high" in col.lower(): rename_map[col] = "High"
            elif "low" in col.lower(): rename_map[col] = "Low"
        df = df.rename(columns=rename_map)

        for col in ["Close","Volume","Open","High","Low"]:
            if col in df.columns:
                df[col] = pd.Series(df[col].values.flatten())

        return df
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None
