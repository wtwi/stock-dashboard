from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os

from analyzer.signals import detect_signals, calculate_indicators
from analyzer.plotting import plot_stock_with_signals
from analyzer.data import get_stock_data
from analyzer.tickers import TICKER_GROUPS, TICKER_NAMES

app = FastAPI()

# ✅ Use absolute paths for Render compatibility
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    charts, signals_by_sector, sector_summary = {}, {}, {}

    for sector, tickers in TICKER_GROUPS.items():
        charts[sector], signals_by_sector[sector], sector_summary[sector] = [], {}, []
        for ticker in tickers:
            try:
                df = get_stock_data(ticker)
                if df is None or df.empty:
                    continue

                df = calculate_indicators(df)
                signals = detect_signals(df)
                chart_file = plot_stock_with_signals(df, signals, ticker)

                charts[sector].append({"ticker": ticker, "chart": chart_file})
                signals_by_sector[sector][ticker] = signals

                if signals:
                    last_signal = signals[-1]
                    sector_summary[sector].append({
                        "ticker": ticker,
                        "action": last_signal["action"],
                        "type": last_signal["type"],
                        "date": last_signal["date"].strftime("%Y-%m-%d"),
                        "price": f"{last_signal['price']:.2f}"
                    })
            except Exception as e:
                print(f"Skipping {ticker}: {e}")

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
