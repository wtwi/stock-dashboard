from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import asyncio

from analyzer.signals import detect_signals
from analyzer.indicators import calculate_indicators
from analyzer.plotting import plot_stock_with_signals
from analyzer.data import get_stock_data_cached
from analyzer.tickers import TICKER_GROUPS, TICKER_NAMES

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")


async def process_ticker(ticker: str):
    try:
        df = get_stock_data_cached(ticker)
        if df is None or df.empty:
            return None

        # Indicators + signals
        df = calculate_indicators(df)
        signals = detect_signals(df)

        # Chart
        chart_file = plot_stock_with_signals(df, signals, ticker)

        # Always include a summary row
        last_price = float(df["Close"].iloc[-1])
        summary = {
            "ticker": ticker,
            "price": f"{last_price:.2f}",
            "target": f"{last_price * 1.1:.2f}",  # fallback target
        }

        # If signals exist, override with last signal info
        if signals:
            last_signal = signals[-1]
            summary.update({
                "price": f"{float(last_signal['price']):.2f}",
                "target": f"{float(last_signal['target']):.2f}",
                "action": last_signal["action"],
                "type": last_signal["type"],
                "date": last_signal["date"].strftime("%Y-%m-%d"),
            })

        return {
            "ticker": ticker,
            "chart": chart_file,
            "signals": signals,
            "summary": summary,
        }

    except Exception as e:
        print(f"Skipping {ticker}: {e}")
        return None


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    charts = {}
    signals_by_sector = {}
    sector_summary = {}

    for sector, tickers in TICKER_GROUPS.items():
        tasks = [process_ticker(t) for t in tickers]
        results = await asyncio.gather(*tasks)

        charts[sector] = []
        signals_by_sector[sector] = {}
        sector_summary[sector] = []

        for result in results:
            if not result:
                continue

            charts[sector].append({
                "ticker": result["ticker"],
                "chart": result["chart"]
            })

            signals_by_sector[sector][result["ticker"]] = result["signals"]

            if result["summary"]:
                sector_summary[sector].append(result["summary"])

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "charts": charts,
            "signals": signals_by_sector,
            "summary": sector_summary,
            "ticker_names": TICKER_NAMES
        }
    )
