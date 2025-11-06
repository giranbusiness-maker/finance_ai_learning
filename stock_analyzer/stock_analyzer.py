import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 1) Részvények listája
tickers = ["AAPL", "MSFT", "SPY"]

# 2) Adatok letöltése az elmúlt 3 hónapra
data = yf.download(tickers, period="3mo")["Close"]

# 3) Hozam számítás (%)
returns = data.pct_change() * 100

# 4) Átlaghozam és volatilitás
summary = pd.DataFrame({
    "Avg Return (%)": returns.mean(),
    "Volatility (%)": returns.std()
})

print("📊 Summary:\n", summary.round(2))

# 5) Grafikon
plt.figure(figsize=(12, 6))
for ticker in tickers:
    plt.plot(data.index, data[ticker], label=ticker)
plt.title("Stock Price Comparison (AAPL vs MSFT vs SPY)")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("stock_comparison_chart.png", dpi=150)
print("✅ Grafikon mentve: stock_comparison_chart.png")

# 6) Mentés Excelbe
summary.to_excel("stock_summary.xlsx")
print("✅ Összefoglaló mentve: stock_summary.xlsx")
from pathlib import Path

# ... a summary DataFrame már létrejött eddigre
out_dir = Path(__file__).parent
xlsx_path = out_dir / "stock_summary.xlsx"
csv_path = out_dir / "stock_summary.csv"

# Biztos mentés: próbáld XLSX-be, ha nem megy, ments CSV-be
try:
    summary.to_excel(xlsx_path, engine="openpyxl")
    print(f"✅ Összefoglaló mentve: {xlsx_path}")
except Exception as e:
    summary.to_csv(csv_path)
    print(f"⚠️ XLSX mentés nem sikerült ({e}). CSV-ként elmentve: {csv_path}")
