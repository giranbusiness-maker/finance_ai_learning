import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Finance Dashboard v1", layout="wide")
st.title("📊 Finance Dashboard v1")
st.caption("Bitcoin + Stocks (AAPL, MSFT, SPY) — native Streamlit charts")

# Sidebar
st.sidebar.header("Settings")
period = st.sidebar.selectbox("Select period", ["1mo", "3mo", "6mo", "1y"], index=1)

# --- BTC SECTION ---
st.header("💰 Bitcoin (BTC-USD)")
try:
    btc = yf.download("BTC-USD", period=period, progress=False, auto_adjust=True)
    if btc.empty:
        st.warning("No BTC data returned. Try another period or check your internet.")
    else:
        btc["SMA7"] = btc["Close"].rolling(7).mean()
        st.subheader("BTC Close & 7-Day SMA")
        st.line_chart(btc[["Close", "SMA7"]])
        st.subheader("Latest rows")
        st.dataframe(btc.tail(5))
except Exception as e:
    st.error(f"BTC section error: {e}")

st.divider()

# --- STOCKS SECTION ---
st.header("📈 Stock Comparison (AAPL, MSFT, SPY)")
tickers = ["AAPL", "MSFT", "SPY"]
try:
    data = yf.download(tickers, period=period, progress=False, auto_adjust=True)["Close"]
    if isinstance(data, pd.Series):
        data = data.to_frame()
    if data.empty:
        st.warning("No stock data returned.")
    else:
        st.subheader("Normalized Performance (=100 at start)")
        norm = data / data.iloc[0] * 100
        st.line_chart(norm)

        returns = data.pct_change() * 100
        summary = pd.DataFrame({
            "Avg Return (%)": returns.mean(),
            "Volatility (%)": returns.std()
        }).round(2)
        st.subheader("Summary")
        st.dataframe(summary)
except Exception as e:
    st.error(f"Stocks section error: {e}")

st.success("✅ Render complete")


