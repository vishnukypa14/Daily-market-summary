import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import requests
import os
from matplotlib import rcParams

rcParams["font.family"] = "DejaVu Sans"


def draw_index(y, name, close, pct):
    arrow = "▲" if pct >= 0 else "▼"
    color = "#2ecc71" if pct >= 0 else "#e74c3c"

    plt.text(0.1, y, f"{name} :", fontsize=13, color="#cae8ff", fontweight="bold")
    plt.text(
        0.4, y,
        f"{close} ({round(pct,2)}%) {arrow}",
        fontsize=13,
        color=color
    )


def draw_flow(y, label, value):
    color = "#2ecc71" if value >= 0 else "#e74c3c"
    plt.text(0.12, y, f"{label} :", fontsize=12, color="#cae8ff", fontweight="bold")
    plt.text(0.4, y, f"{value} Cr", fontsize=12, color=color)



def get_index_data(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="2d")

    close_today = data["Close"].iloc[-1]
    close_yesterday = data["Close"].iloc[-2]

    change = close_today - close_yesterday
    pct_change = (change / close_yesterday) * 100

    return round(close_today,2), round(change,2), round(pct_change,2)


def get_fii_dii():
    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json",
            "Referer": "https://www.nseindia.com"
        }

        session = requests.Session()
        session.get("https://www.nseindia.com", headers=headers)

        url = "https://www.nseindia.com/api/fiidiiTradeReact"
        response = session.get(url, headers=headers, timeout=10)

        data = response.json()
        df = pd.DataFrame(data)

        fii = df[df["category"] == "FII/FPI"].iloc[0]
        dii = df[df["category"] == "DII"].iloc[0]

        return float(fii["netValue"]), float(dii["netValue"])

    except Exception as e:
        print("FII/DII fetch failed:", e)
        return None, None


nifty = get_index_data("^NSEI")
sensex = get_index_data("^BSESN")
banknifty = get_index_data("^NSEBANK")

fii_net, dii_net = get_fii_dii()


rows = [
    ["NIFTY 50", *nifty],
    ["SENSEX", *sensex],
    ["BANK NIFTY", *banknifty]
]

if fii_net is not None:
    rows.append(["FII (₹ Cr)", "-", fii_net, ""])

if dii_net is not None:
    rows.append(["DII (₹ Cr)", "-", dii_net, ""])

summary = pd.DataFrame(
    rows,
    columns=["Index", "Close", "Change", "Change %"]
)

fig = plt.figure(figsize=(6, 8), facecolor="black")
plt.axis("off")

plt.text(
    0.5, 0.92,
    "Market Summary Report",
    ha="center",
    fontsize=18,
    color="#cae8ff",
    fontweight="bold"
)

plt.text(
    0.5, 0.88,
    datetime.now().strftime("%d %b %Y"),
    ha="center",
    fontsize=12,
    color="#9b59b6"
)

draw_index(0.78, "NIFTY", nifty[0], nifty[2])
draw_index(0.72, "BANK NIFTY", banknifty[0], banknifty[2])
draw_index(0.66, "SENSEX", sensex[0], sensex[2])

plt.text(
    0.1, 0.55,
    "FII & DIIs Data",
    fontsize=14,
    color="#cae8ff",
    fontweight="bold"
)

if fii_net is not None:
    draw_flow(0.48, "FII", fii_net)

if dii_net is not None:
    draw_flow(0.42, "DII", dii_net)

plt.savefig(
    "daily_market_report.png",
    dpi=200,
    bbox_inches="tight",
    facecolor=fig.get_facecolor()
)
plt.close()

