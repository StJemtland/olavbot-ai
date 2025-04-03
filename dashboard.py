def hent_data(ticker):
    data = yf.download(ticker, period="5d", interval="1h")
    if data.empty or "Close" not in data.columns:
        return {
            "labels": [],
            "values": []
        }

    close_values = data["Close"]
    if close_values.empty:
        return {
            "labels": [],
            "values": []
        }

    return {
        "labels": data.index.strftime("%d.%m %H:%M").tolist(),
        "values": close_values.round(2).tolist()
    }

