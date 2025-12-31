import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os



def get_index_data(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="2d")

    close_today = data["Close"].iloc[-1]
    close_yesterday = data["Close"].iloc[-2]

    change = close_today - close_yesterday
    pct_change = (change / close_yesterday) * 100

    return round(close_today,2), round(change,2), round(pct_change,2)


nifty = get_index_data("^NSEI")
sensex = get_index_data("^BSESN")
banknifty = get_index_data("^NSEBANK")


summary = pd.DataFrame([
    ["NIFTY 50", *nifty],
    ["SENSEX", *sensex],
    ["BANK NIFTY", *banknifty]
], columns=["Index", "Close", "Change", "Change %"])


plt.figure(figsize=(8, 4))
plt.axis("off")

plt.title(
    f"Market Closing Report – {datetime.now().strftime('%d %b %Y')}",
    fontsize=14,
    pad=20
)

table = plt.table(
    cellText=summary.values,
    colLabels=summary.columns,
    loc="center",
    cellLoc="center"
)

for i in range(len(summary)):
    color = "#2ecc71" if summary.iloc[i]["Change %"] >= 0 else "#e74c3c"
    table[(i+1, 3)].set_text_props(color=color)

table.scale(1, 1.5)
plt.savefig("daily_market_report.png", bbox_inches="tight", dpi=200)
print("Image generated:", os.path.exists("daily_market_report.png"))

