import matplotlib
matplotlib.use("TkAgg")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import yfinance as yf

# ✅ Dine valgte aktiva
crypto_coins = ['XRP-USD', 'ETH-USD', 'BTC-USD']
stock_symbols = ['KOG.OL', 'SAAB-B.ST', 'NHY.OL']
all_assets = crypto_coins + stock_symbols

start_cash = 1000
days = 90

# Last ned data
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=days)
price_data = {}

for asset in all_assets:
    df = yf.download(asset, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
    df = df[['Close']].dropna()
    df.columns = [asset]
    price_data[asset] = df

# Kombiner alle i én DataFrame
combined = pd.concat(price_data.values(), axis=1)
combined.dropna(inplace=True)

# RSI-funksjon
def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Simulering
portfolio_value = []
portfolio_log = []
decision_log = []
cash = start_cash
holdings = {asset: 0 for asset in all_assets}
ma_short = 10
ma_long = 30
trade_fraction = 0.3  # 30 % av cash per handel

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

            # KJØP
            if rsi < 30 and ma_10 < ma_30 and cash > 0:
                invest_amount = cash * trade_fraction
                holdings[asset] += invest_amount / price
                cash -= invest_amount
                action_taken = f"KJØPTE {asset} for {round(invest_amount,2)}"
                explanation = "RSI < 30 og MA10 < MA30"
                portfolio_log.append(f"{date.date()}: {action_taken} (RSI: {round(rsi,1)}, MA10 < MA30)")

            # SELG
            elif rsi > 70 and ma_10 > ma_30 and holdings[asset] > 0:
                sell_value = holdings[asset] * price
                cash += sell_value
                action_taken = f"SOLGTE {asset} for {round(sell_value,2)}"
                explanation = "RSI > 70 og MA10 > MA30"
                holdings[asset] = 0
                portfolio_log.append(f"{date.date()}: {action_taken} (RSI: {round(rsi,1)}, MA10 > MA30)")

            else:
                explanation = f"RSI={round(rsi,1)}, MA10={round(ma_10,2)}, MA30={round(ma_30,2)} – ingen signaler"

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

# DataFrames
value_df = pd.DataFrame(portfolio_value, columns=['Date', 'Value']).set_index('Date')
log_df = pd.DataFrame(portfolio_log, columns=["Transaksjoner"])
decision_df = pd.DataFrame(decision_log)

# Graf
plt.figure(figsize=(12, 6))
plt.plot(value_df.index, value_df['Value'], label='Porteføljeverdi', linewidth=2)
plt.title('AI Bot v5 – Hybrid strategi – Krypto + Skandinaviske aksjer')
plt.xlabel('Dato')
plt.ylabel('Verdi (USD)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Print logg i terminalen
print("\n--- TRANSAKSJONSLOGG ---")
for log in portfolio_log:
    print(log)

print(f"\nSluttverdi på porteføljen: {round(value_df['Value'].iloc[-1], 2)} USD")

# Lagre logg til filer
decision_df.to_csv("beslutningslogg_v5.csv", index=False)
log_df.to_csv("transaksjonslogg_v5.csv", index=False)
