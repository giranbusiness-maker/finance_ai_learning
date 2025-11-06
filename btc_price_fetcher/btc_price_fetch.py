import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 1) Adatlehívás: utolsó 3 hónap BTC
btc = yf.Ticker("BTC-USD")
data = btc.history(period="3mo")

# 2) Ellenőrzés
if data.empty:
    raise ValueError("No BTC data received. Try again later.")

# 3) 7 napos mozgóátlag
data["SMA7"] = data["Close"].rolling(window=7).mean()

# 4) CSV mentés
data.to_csv("btc_data.csv", index=True)
print("✅ Adatok lementve: btc_data.csv")

# 5) Grafikon mentés PNG-be (nem nyit ablakot, csak ment)
plt.figure(figsize=(12, 6))
plt.plot(data.index, data["Close"], label="BTC Close")
plt.plot(data.index, data["SMA7"], label="SMA 7", linestyle="--")
plt.title("BTC - Close & 7-Day SMA (last 3 months)")
plt.xlabel("Date")
plt.ylabel("USD")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("btc_price_chart.png", dpi=150)
print("✅ Grafikon mentve: btc_price_chart.png")

