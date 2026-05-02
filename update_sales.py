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

def fetch_alaska():

    url = "https://storefront.points.com/mileage-plan/en-US/buy"

    try:

        r = requests.get(url, timeout=20)

        text = r.text

        bonus_match = re.search(
            r'(\d+)%\\s*bonus',
            text,
            re.I
        )

        if bonus_match:
            bonus = bonus_match.group(1) + "%"
        else:
            bonus = "Unknown"

        return {
            "program": "Alaska",
            "bonus": bonus,
            "min_buy": 20000,
            "usd_cost": 591.25,
            "received": 32000,
            "end": "Check Website"
        }

    except Exception as e:

        print("Alaska error", e)

        return None
def fetch_ihg():
    url = "https://storefront.points.com/ihg-rewards/en-US/buy"

    try:
        r = requests.get(url, timeout=20)
        text = r.text

        bonus_match = re.search(r'(\d+)%\s*bonus', text, re.I)

        if bonus_match:
            bonus = bonus_match.group(1) + "%"
        else:
            bonus = "Unknown"

        return {
            "program": "IHG",
            "bonus": bonus,
            "min_buy": 26000,
            "usd_cost": 260,
            "received": 52000,
            "end": "Check Website"
        }

    except Exception as e:
        print("IHG error", e)
        return None

def fetch_flyingblue():
    url = "https://storefront.points.com/flyingblue/en-US/buy"

    try:
        r = requests.get(url, timeout=20)
        text = r.text

        bonus_match = re.search(r'(\d+)%\s*bonus', text, re.I)

        if bonus_match:
            bonus = bonus_match.group(1) + "%"
        else:
            bonus = "Unknown"

        return {
            "program": "FlyingBlue",
            "bonus": bonus,
            "min_buy": 24000,
            "usd_cost": 660,
            "received": 43200,
            "end": "Check Website"
        }

    except Exception as e:
        print("FlyingBlue error", e)
        return None

def fetch_choice():
    url = "https://storefront.points.com/choice-privileges/en-US/buy"

    try:
        r = requests.get(url, timeout=20)
        text = r.text

        bonus_match = re.search(r'(\d+)%\s*bonus', text, re.I)

        if bonus_match:
            bonus = bonus_match.group(1) + "%"
        else:
            bonus = "Unknown"

        return {
            "program": "Choice",
            "bonus": bonus,
            "min_buy": 8000,
            "usd_cost": 88,
            "received": 11200,
            "end": "Check Website"
        }

    except Exception as e:
        print("Choice error", e)
        return None

sales = []
programs = [
    fetch_alaska(),
    fetch_ihg(),
    fetch_flyingblue(),
    fetch_choice()
]

for p in programs:

    if not p:
        continue

    twd_cost = p["usd_cost"] * usd_twd * (1 + fee)
    cpp = round(twd_cost / p["received"], 3)

    sales.append({
        "program": p["program"],
        "bonus": p["bonus"],
        "min_buy": p["min_buy"],
        "usd_cost": p["usd_cost"],
        "fee": fee,
        "twd_cost": round(twd_cost),
        "received": p["received"],
        "cpp": cpp,
        "end": p["end"]
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
