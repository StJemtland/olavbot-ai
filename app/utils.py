import yfinance as yf

def hent_data(ticker):
    try:
        data = yf.download(ticker, period="5d", interval="1h")
        if data.empty or "Close" not in data.columns:
            return {"labels": [], "values": []}
        return {
            "labels": data.index.strftime("%d.%m %H:%M").tolist(),
            "values": data["Close"].round(2).tolist()
        }
    except Exception as e:
        print(f"Feil ved henting av {ticker}: {e}")
        return {"labels": [], "values": []}


