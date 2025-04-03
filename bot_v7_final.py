import smtplib
from email.mime.text import MIMEText
import pandas as pd
import numpy as np
import datetime
import yfinance as yf
import sys

# 📩 E-postfunksjon
def send_email(subject, body):
    sender = "petitpatrickpetit@gmail.com"
    mottaker = "petitpatrickpetit@gmail.com"
    app_passord = "kcfyiqyorustrtdf"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = mottaker

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, app_passord)
            server.send_message(msg)
        print("✅ E-post sendt!")
    except Exception as e:
        print("❌ E-postfeil:", e)

# 📊 Aktiva
krypto = ['BTC-USD', 'ETH-USD', 'XRP-USD']
aksjer = ['KOG.OL', 'NHY.OL', 'SAAB-B.ST']
alle = krypto + aksjer

# 📅 Tidspunkt
nå = datetime.datetime.now()
tid = nå.strftime('%H:%M')
vis_rapport = "view" in sys.argv
er_riktig_tid = tid in ["06:45", "20:00"]

# 🚫 Ikke kjør med mindre det er tid eller manuelt "view"
if not er_riktig_tid and not vis_rapport:
    print("🧘‍♂️ Ikke rapporttid. Boten gjør ingenting.")
    exit()

# 📦 Hent data
start_cash = 1000
slutt = datetime.datetime.now()
start = slutt - datetime.timedelta(days=90)

data = {}
for ticker in alle:
    df = yf.download(ticker, start=start.strftime('%Y-%m-%d'), end=slutt.strftime('%Y-%m-%d'))
    df = df[['Close']].dropna()
    df.columns = [ticker]
    data[ticker] = df

kombinert = pd.concat(data.values(), axis=1)
kombinert.dropna(inplace=True)

# RSI-funksjon
def beregn_rsi(series, periode=14):
    delta = series.diff()
    gevinst = delta.where(delta > 0, 0.0)
    tap = -delta.where(delta < 0, 0.0)
    snitt_gevinst = gevinst.rolling(window=periode).mean()
    snitt_tap = tap.rolling(window=periode).mean()
    rs = snitt_gevinst / snitt_tap
    return 100 - (100 / (1 + rs))

# 🚀 Simulering
cash = start_cash
holdings = {ticker: 0 for ticker in alle}
logg = []

for dato, rad in kombinert.iterrows():
    for ticker in alle:
        pris = rad[ticker]
        rsi = beregn_rsi(kombinert[ticker]).loc[dato]
        ma_10 = kombinert[ticker].rolling(window=10).mean().loc[dato]
        ma_30 = kombinert[ticker].rolling(window=30).mean().loc[dato]

        handling = None
        if pd.notna(rsi) and pd.notna(ma_10) and pd.notna(ma_30):
            if rsi < 30 and ma_10 < ma_30 and cash > 0:
                beløp = cash * 0.3
                holdings[ticker] += beløp / pris
                cash -= beløp
                handling = f"KJØPTE {ticker} for {round(beløp,2)}"
            elif rsi > 70 and ma_10 > ma_30 and holdings[ticker] > 0:
                verdi = holdings[ticker] * pris
                cash += verdi
                holdings[ticker] = 0
                handling = f"SOLGTE {ticker} for {round(verdi,2)}"

        if handling:
            logg.append(f"{dato.date()} | {handling} | RSI: {round(rsi,1)} | Pris: {round(pris,2)}")
        elif rsi < 25 or rsi > 75:
            logg.append(f"{dato.date()} | SIGNAL: {ticker} har RSI {round(rsi,1)} | Pris: {round(pris,2)}")

# 📤 Rapporter
if logg:
    rapport = "📊 AI-BOT RAPPORT\n\n" + "\n".join(logg)
else:
    rapport = "🧠 AI-boten har analysert markedet. Ingen sterke signaler eller handler i dag."

# 👀 Vis eller send
if vis_rapport:
    print(rapport)
else:
    send_email("📩 AI-BOT DAGSRAPPORT", rapport)

