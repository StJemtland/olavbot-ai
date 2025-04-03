from flask import Flask, render_template
import yfinance as yf
import datetime

app = Flask(__name__)

def hent_data(ticker):
    data = yf.download(ticker, period="5d", interval="1h")
    if data.empty or "Close" not in data.columns:
        return {
            "labels": [],
            "values": []
        }
    return {
        "labels": data.index.strftime("%d.%m %H:%M").tolist(),
        "values": data["Close"].round(2).tolist()  # ✅ Riktig metode
    }

@app.route("/")
def index():
    aksjer = {
        "KOG": hent_data("KOG.OL"),
        "NHY": hent_data("NHY.OL"),
        "SAAB-B.ST": hent_data("SAAB-B.ST")
    }

    krypto = {
        "XRP": hent_data("XRP-USD"),
        "ETH": hent_data("ETH-USD"),
        "BTC": hent_data("BTC-USD")
    }

    return render_template("index.html", aksjer=aksjer, krypto=krypto, tidspunkt=datetime.datetime.now().strftime("%d.%m %H:%M"))

if __name__ == "__main__":
    app.run()

