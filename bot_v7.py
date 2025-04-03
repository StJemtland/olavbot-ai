import matplotlib
matplotlib.use("TkAgg")

import smtplib
from email.mime.text import MIMEText
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import yfinance as yf
import time

# 📩 Send e-post
def send_email(subject, body):
    sender_email = "petitpatrickpetit@gmail.com"
    receiver_email = "petitpatrickpetit@gmail.com"
    app_password = "kcfyiqyorustrtdf"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        print("✅ E-post sendt!")
    except Exception as e:
        print("❌ E-postfeil:", e)

# 🌍 Aktiva
crypto_list = ['BTC-USD', 'ETH-USD', 'XRP-USD']
stock_list = ['KOG.OL', 'NHY.OL', 'SAAB-B.ST']
all_assets = crypto_list + stock_list

start_cash = 1000
days = 90
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=days)

price_data = {}
for asset in all_assets:
    df = yf.download(asset, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
    df = df[['Close']].dropna()
    df.columns = [asset]
    price_data[asset] = df

combined = pd.concat(price_data.values(), axis=1)
combined.dropna(inplace=True)

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

portfolio_value = []
portfolio_log = []
decision_log = []
email_log = []
cash = start_cash
holdings = {asset: 0 for asset in all_assets}
ma_short = 10
ma_long = 30
trade_fraction = 0.3

for date, row in combined.iterrows():
    for asset in all_assets:
        rsi_series = compute_rsi(combined[asset])
        rsi = rsi_series.loc[date]
        price = row[asset]
        ma_10 = combined[asset].rolling(window=ma_short).mean().loc[date]
        ma_30 = combined[asset].rolling(window=ma_long).mean().loc[date]

        if pd.notna(rsi) and pd.notna(ma_10) and pd.notna(ma_30):
            action_taken = "Ingen handling"
            explanation = ""

            # 🚨 Ekstra sterk varsel
            if rsi < 25 or rsi > 75:
                send_email(
                    "🚨 AI-BOT VARSEL",
                    f"Sterkt signal: {asset} har RSI {round(rsi,1)}!\nPris: {round(price,2)}"
                )

            if rsi < 30 and ma_10 < ma_30 and cash > 0:
                invest_amount = cash * trade_fraction
                holdings[asset] += invest_amount / price
                cash -= invest_amount
                action_taken = f"KJØPTE {asset} for {round(invest_amount,2)}"
                explanation = "RSI < 30 og MA10 < MA30"
                portfolio_log.append(f"{date.date()}: {action_taken} (RSI: {round(rsi,1)}, MA10 < MA30)")
                email_log.append(f"{action_taken} | RSI: {round(rsi,1)} | Pris: {round(price,2)}")

            elif rsi > 70 and ma_10 > ma_30 and holdings[asset] > 0:
                sell_value = holdings[asset] * price
                cash += sell_value
                holdings[asset] = 0
                action_taken = f"SOLGTE {asset} for {round(sell_value,2)}"
                explanation = "RSI > 70 og MA10 > MA30"
                portfolio_log.append(f"{date.date()}: {action_taken} (RSI: {round(rsi,1)}, MA10 > MA30)")
                email_log.append(f"{action_taken} | RSI: {round(rsi,1)} | Pris: {round(price,2)}")

            decision_log.append({
                "Dato": date.date(),
                "Asset": asset,
                "RSI": round(rsi, 1),
                "MA10": round(ma_10, 2),
                "MA30": round(ma_30, 2),
                "Pris": round(price, 2),
                "Handling": action_taken,
                "Forklaring": explanation
            })

    value = cash + sum(holdings[c] * row[c] for c in all_assets)
    portfolio_value.append((date, value))

# ⏰ Sjekk klokkeslett for fast rapport
now = datetime.datetime.now()
if now.strftime('%H:%M') in ['06:45', '20:00']:
    if email_log:
        body = "📈 AI Dagsrapport:\n\n" + "\n".join(email_log)
    else:
        body = "🧠 AI har vurdert markedet.\nIngen handler i dag."
    send_email("📩 AI-BOT DAGSRAPPORT", body)

# Lagre til fil
pd.DataFrame(portfolio_log, columns=["Transaksjoner"]).to_csv("transaksjonslogg_v7.csv", index=False)
pd.DataFrame(decision_log).to_csv("beslutningslogg_v7.csv", index=False)

