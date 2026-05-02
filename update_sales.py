import json
import requests
from datetime import date

# 即時匯率
fx = requests.get(
    "https://open.er-api.com/v6/latest/USD"
).json()

usd_twd = fx["rates"]["TWD"]

fee = 0.015

sales = []

# Alaska (目前示範資料)
bonus = "60%"
min_buy = 20000
usd_cost = 591.25
received = 32000

twd_cost = usd_cost * usd_twd * (1 + fee)
cpp = round(twd_cost / received, 3)

sales.append({
    "program": "Alaska",
    "bonus": bonus,
    "min_buy": min_buy,
    "usd_cost": usd_cost,
    "fee": fee,
    "twd_cost": round(twd_cost),
    "received": received,
    "cpp": cpp,
    "end": "2026-05-30"
})

# IHG (目前示範資料)
bonus = "100%"
min_buy = 26000
usd_cost = 260
received = 52000

twd_cost = usd_cost * usd_twd * (1 + fee)
cpp = round(twd_cost / received, 3)

sales.append({
    "program": "IHG",
    "bonus": bonus,
    "min_buy": min_buy,
    "usd_cost": usd_cost,
    "fee": fee,
    "twd_cost": round(twd_cost),
    "received": received,
    "cpp": cpp,
    "end": "2026-05-25"
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
