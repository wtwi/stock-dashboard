import yfinance as yf
from functools import lru_cache
import time

CACHE_TTL = 3600  # 1 hour


@lru_cache(maxsize=512)
def _cached_download(key):
    ticker = key.split("_")[0]
    return yf.download(ticker, period="2y", progress=False)


def get_stock_data_cached(ticker):
    """Cache stock data for 1 hour."""
    now = int(time.time())
    key = f"{ticker}_{now // CACHE_TTL}"
    return _cached_download(key)
