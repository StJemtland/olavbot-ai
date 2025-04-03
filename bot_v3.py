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

# Simulering med forbedret strategi
portfolio_value = []
portfolio_log = []
cash = start_cash
holdings = {coin: 0 for coin in coins}
ma_short = 20
ma_long = 50
trade_fraction = 0.25  # Invester 25 % av tilgjengelig cash

for date, row in combined.iterrows():
    for coin in coins:
        rsi_series = compute_rsi(combined[coin])
        rsi = rsi_series.loc[date]
        price = row[coin]
        ma_20 = combined[coin].rolling(window=ma_short).mean().loc[date]
        ma_50 = combined[coin].rolling(window=ma_long).mean().loc[date]

        if pd.notna(rsi) and pd.notna(ma_20) and pd.notna(ma_50):
            # KJØP: RSI < 25, MA20 < MA50
            if rsi < 25 and ma_20 < ma_50 and cash > 0:
                invest_amount = cash * trade_fraction
                holdings[coin] += invest_amount / price
                cash -= invest_amount
                portfolio_log.append(f"{date.date()}: KJØPTE {coin} for {round(invest_amount,2)} (RSI: {round(rsi,1)}, MA20 < MA50)")

            # SELG: RSI > 70 og MA20 > MA50
            elif rsi > 70 and ma_20 > ma_50 and holdings[coin] > 0:
                sell_value = holdings[coin] * price
                cash += sell_value
                portfolio_log.append(f"{date.date()}: SOLGTE {coin} for {round(sell_value,2)} (RSI: {round(rsi,1)}, MA20 > MA50)")
                holdings[coin] = 0

    # Oppdater porteføljeverdi
    value = cash + sum(holdings[c] * row[c] for c in coins)
    portfolio_value.append((date, value))

# Lag DataFrame for verdi
value_df = pd.DataFrame(portfolio_value, columns=['Date', 'Value']).set_index('Date')

# Plot porteføljeverdi
plt.figure(figsize=(12, 6))
plt.plot(value_df.index, value_df['Value'], label='Porteføljeverdi', linewidth=2)
plt.title('AI Bot v3 – RSI < 25 + MA-trend + 25% cash per trade – Start: 1000 kr')
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
