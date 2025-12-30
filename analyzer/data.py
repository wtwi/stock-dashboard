import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import yfinance as yf
import pandas as pd
import numpy as np
from functools import lru_cache

@lru_cache(maxsize=256)
def get_stock_data_cached(ticker: str) -> pd.DataFrame:
    try:
        df = yf.download(ticker, period="2y", progress=False)

        if df is None or df.empty:
            print(f"Skipping {ticker}: no data returned")
            return None

        # ---------------------------------------------------------
        # 1. Normalize column names (fix MultiIndex AND list columns)
        # ---------------------------------------------------------
        new_cols = []
        for col in df.columns:
            if isinstance(col, (list, tuple, np.ndarray)):
                # Convert ['Close'] → 'Close'
                col = col[0]
            if isinstance(col, tuple):
                # Convert ('Close','') → 'Close'
                col = col[0]
            new_cols.append(str(col))

        df.columns = new_cols

        # ---------------------------------------------------------
        # 2. Reset index so Date becomes a column
        # ---------------------------------------------------------
        df = df.reset_index()

        # ---------------------------------------------------------
        # 3. Flatten nested values inside rows
        # ---------------------------------------------------------
        for col in df.columns:
            df[col] = df[col].apply(
                lambda x: x[0] if isinstance(x, (list, tuple, np.ndarray)) else x
            )

        # ---------------------------------------------------------
        # 4. Ensure OHLCV columns are numeric floats
        # ---------------------------------------------------------
        numeric_cols = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # ---------------------------------------------------------
        # 5. Drop rows with missing Close prices
        # ---------------------------------------------------------
        df = df.dropna(subset=["Close"])

        if df.empty:
            print(f"Skipping {ticker}: all rows invalid after cleaning")
            return None

        return df

    except Exception as e:
        print(f"Skipping {ticker}: {e}")
        return None
