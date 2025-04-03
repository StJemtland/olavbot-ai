import matplotlib
matplotlib.use("TkAgg")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import yfinance as yf

# Coins og innstillinger
coins = ['BTC-USD', 'ETH-USD', 'SOL-USD']
start_cash = 1000
days = 90

# Last ned data
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=days)
price_data = {}

for coin in coins:
    df = yf.download(coin, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
    df = df[['Close']].dropna()
    df.columns = [coin]
    price_data[coin] = df

# Kombiner alle coins i én DataFrame
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

# Simulering med forklaringer
portfolio_value = []
portfolio_log = []
decision_log = []
cash = start_cash
holdings = {coin: 0 for coin in coins}
ma_short = 20
ma_long = 50
trade_fraction = 0.25

for date, row in combined.iterrows():
    for coin in coins:
        rsi_series = compute_rsi(combined[coin])
        rsi = rsi_series.loc[date]
        price = row[coin]
        ma_20 = combined[coin].rolling(window=ma_short).mean().loc[date]
        ma_50 = combined[coin].rolling(window=ma_long).mean().loc[date]

        if pd.notna(rsi) and pd.notna(ma_20) and pd.notna(ma_50):
            action_taken = "Ingen handling"
            explanation = ""

            if rsi < 25 and ma_20 < ma_50 and cash > 0:
                invest_amount = cash * trade_fraction
                holdings[coin] += invest_amount / price
                cash -= invest_amount
                action_taken = f"KJØPTE {coin} for {round(invest_amount,2)}"
                explanation = "RSI < 25 og MA20 < MA50"
                portfolio_log.append(f"{date.date()}: {action_taken} (RSI: {round(rsi,1)}, MA20 < MA50)")

            elif rsi > 70 and ma_20 > ma_50 and holdings[coin] > 0:
                sell_value = holdings[coin] * price
                cash += sell_value
                action_taken = f"SOLGTE {coin} for {round(sell_value,2)}"
                explanation = "RSI > 70 og MA20 > MA50"
                holdings[coin] = 0
                portfolio_log.append(f"{date.date()}: {action_taken} (RSI: {round(rsi,1)}, MA20 > MA50)")

            else:
                explanation = f"RSI={round(rsi,1)}, MA20={round(ma_20,2)}, MA50={round(ma_50,2)} – ingen klare signaler"

            decision_log.append({
                "Dato": date.date(),
                "Coin": coin,
                "RSI": round(rsi, 1),
                "MA20": round(ma_20, 2),
                "MA50": round(ma_50, 2),
                "Pris": round(price, 2),
                "Handling": action_taken,
                "Forklaring": explanation
            })

    value = cash + sum(holdings[c] * row[c] for c in coins)
    portfolio_value.append((date, value))

# DataFrames
value_df = pd.DataFrame(portfolio_value, columns=['Date', 'Value']).set_index('Date')
log_df = pd.DataFrame(portfolio_log, columns=["Transaksjoner"])
decision_df = pd.DataFrame(decision_log)

# Plot verdi
plt.figure(figsize=(12, 6))
plt.plot(value_df.index, value_df['Value'], label='Porteføljeverdi', linewidth=2)
plt.title('AI Bot v4 – RSI + MA + Forklaring – Start 1000 kr')
plt.xlabel('Dato')
plt.ylabel('Verdi (USD)')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# Vis logg i terminalen
print("\n--- TRANSAKSJONSLOGG ---")
for log in portfolio_log:
    print(log)

print(f"\nSluttverdi på porteføljen: {round(value_df['Value'].iloc[-1], 2)} USD")

# Eksporter forklaringer til CSV (valgfritt)
decision_df.to_csv("beslutningslogg.csv", index=False)
log_df.to_csv("transaksjonslogg.csv", index=False)
