import json
import re
import requests
from bs4 import BeautifulSoup
from datetime import date

# 即時匯率
fx = requests.get(
    "https://open.er-api.com/v6/latest/USD"
).json()

usd_twd = fx["rates"]["TWD"]

fee = 0.015

def fetch_blog_sales():

    url = "https://frequentmiler.com/tag/buy-miles-points/"

    sales = []

    try:

        r = requests.get(url, timeout=20)

        soup = BeautifulSoup(r.text, "html.parser")

        titles = " ".join([
            h.get_text(" ", strip=True)
            for h in soup.find_all(["h2", "h3"])
        ])

        programs = [
            ("Alaska", r"Alaska.*?(\d+)%"),
            ("IHG", r"IHG.*?(\d+)%"),
            ("Choice", r"Choice.*?(\d+)%"),
            ("FlyingBlue", r"Flying Blue.*?(\d+)%")
        ]

        for name, pattern in programs:

            match = re.search(pattern, titles, re.I)

            if match:
                bonus = match.group(1) + "%"
            else:
                continue

            sales.append({
                "program": name,
                "bonus": bonus
            })

        return sales

    except Exception as e:

        print("Blog fetch error", e)

        return []

sales = []

blog_sales = fetch_blog_sales()

defaults = {
    "Alaska": {
        "min_buy": 20000,
        "usd_cost": 591.25,
        "received": 32000
    },
    "IHG": {
        "min_buy": 26000,
        "usd_cost": 260,
        "received": 52000
    },
    "FlyingBlue": {
        "min_buy": 24000,
        "usd_cost": 660,
        "received": 43200
    },
    "Choice": {
        "min_buy": 8000,
        "usd_cost": 88,
        "received": 11200
    }
}

for p in blog_sales:

    d = defaults[p["program"]]

    twd_cost = d["usd_cost"] * usd_twd * (1 + fee)

    cpp = round(
        twd_cost / d["received"],
        3
    )

    sales.append({
        "program": p["program"],
        "bonus": p["bonus"],
        "min_buy": d["min_buy"],
        "usd_cost": d["usd_cost"],
        "fee": fee,
        "twd_cost": round(twd_cost),
        "received": d["received"],
        "cpp": cpp,
        "end": "Check Blog"
    })

data = {
    "updated": str(date.today()),
    "fx": {
        "USD_TWD": round(usd_twd, 2)
    },
    "sales": sales
}

with open("sales.json", "w") as f:
    json.dump(data, f, indent=2)

print("sales.json updated")
