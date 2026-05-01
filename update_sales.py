import json
from datetime import date

# 模擬即時匯率
usd_twd = 32.4

# 海外刷卡手續費
fee = 0.015

sales = []

# Alaska
usd_cost = 591.25
received = 32000

twd_cost = usd_cost * usd_twd * (1 + fee)
cpp = round(twd_cost / received, 3)

sales.append({
    "program": "Alaska",
    "bonus": "60%",
    "min_buy": 20000,
    "usd_cost": usd_cost,
    "fee": fee,
    "twd_cost": round(twd_cost),
    "received": received,
    "cpp": cpp,
    "end": "2026-05-30"
})

# IHG
usd_cost = 260
received = 52000

twd_cost = usd_cost * usd_twd * (1 + fee)
cpp = round(twd_cost / received, 3)

sales.append({
    "program": "IHG",
    "bonus": "100%",
    "min_buy": 26000,
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
        "USD_TWD": usd_twd
    },
    "sales": sales
}

with open("sales.json", "w") as f:
    json.dump(data, f, indent=2)

print("sales.json updated")
