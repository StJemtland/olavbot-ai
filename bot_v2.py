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
days = 60

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

# Simulering med RSI + glidende snitt
portfolio_value = []
portfolio_log = []
cash = start_cash
holdings = {coin: 0 for coin in coins}
ma_window = 20  # Glidende gjennomsnitt over 20 dager

for date, row in combined.iterrows():
    for coin in coins:
        rsi = compute_rsi(combined[coin]).loc[date]
        price = row[coin]
        moving_avg = combined[coin].rolling(window=ma_window).mean().loc[date]

        if pd.notna(rsi) and pd.notna(moving_avg):
            # KJØP: RSI < 30 og pris under MA
            if rsi < 30 and price < moving_avg and cash > 0:
                invest_amount = cash / len(coins)
                holdings[coin] += invest_amount / price
                cash -= invest_amount
                portfolio_log.append(f"{date.date()}: KJØPTE {coin} for {round(invest_amount,2)} (RSI: {round(rsi,1)}, Pris under MA)")

            # SELG: RSI > 70 og pris over MA
            elif rsi > 70 and price > moving_avg and holdings[coin] > 0:
                sell_value = holdings[coin] * price
                cash += sell_value
                portfolio_log.append(f"{date.date()}: SOLGTE {coin} for {round(sell_value,2)} (RSI: {round(rsi,1)}, Pris over MA)")
                holdings[coin] = 0

    # Oppdater porteføljeverdi
    value = cash + sum(holdings[c] * row[c] for c in coins)
    portfolio_value.append((date, value))

# Lag DataFrame for verdi
value_df = pd.DataFrame(portfolio_value, columns=['Date', 'Value']).set_index('Date')

# Plot porteføljeverdi
plt.figure(figsize=(12, 6))
plt.plot(value_df.index, value_df['Value'], label='Porteføljeverdi', linewidth=2)
plt.title('AI Bot 2.0 – RSI + Glidende Snitt (MA20) – 1000 kr start')
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
