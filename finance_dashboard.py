import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Finance Dashboard v1", layout="wide")

st.title("📊 Finance Dashboard v1")
st.write("Bitcoin + Stock (AAPL, MSFT, SPY) performance tracker")

# Sidebar
st.sidebar.header("Settings")
period = st.sidebar.selectbox("Select period", ["1mo", "3mo", "6mo", "1y"], index=1)

# --- BTC Section ---
st.header("💰 Bitcoin (BTC-USD)")
btc = yf.Ticker("BTC-USD").history(period=period)
btc["SMA7"] = btc["Close"].rolling(window=7).mean()

fig1, ax1 = plt.subplots(figsize=(10,4))
ax1.plot(btc.index, btc["Close"], label="BTC Close")
ax1.plot(btc.index, btc["SMA7"], label="7-Day SMA", linestyle="--")
ax1.legend()
ax1.set_title("BTC Price")
st.pyplot(fig1)

# --- Stocks Section ---
st.header("📈 Stock Comparison")
tickers = ["AAPL", "MSFT", "SPY"]
data = yf.download(tickers, period=period)["Close"]

fig2, ax2 = plt.subplots(figsize=(10,4))
for ticker in tickers:
    ax2.plot(data.index, data[ticker], label=ticker)
ax2.legend()
ax2.set_title("Stock Prices")
st.pyplot(fig2)

# --- Returns Summary ---
returns = data.pct_change() * 100
summary = pd.DataFrame({
    "Avg Return (%)": returns.mean(),
    "Volatility (%)": returns.std()
}).round(2)

st.header("📊 Summary Table")
st.dataframe(summary)