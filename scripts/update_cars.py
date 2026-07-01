"""
Auto-updates cars.json with new listings from Encar.
Runs daily via GitHub Actions. Edit SEARCH_CONFIG to change filters.
"""

import json
import os
import re
import sys
import requests

# ---------------------------------------------------------------------------
# CONFIGURATION — edit these to match what you want to show on the site
# ---------------------------------------------------------------------------
SEARCH_CONFIG = {
    "min_price_man": 500,    # 만원  →  500 = 5 000 000 KRW  (~2 800 €)
    "max_price_man": 5000,   # 만원  → 5000 = 50 000 000 KRW (~28 000 €)
    "max_mileage":   150000, # km
    "min_year":      2015,
    "fetch_count":   30,     # how many recent listings to scan per run
}

# Korean brand name → English display name
BRAND_MAP = {
    "벤츠":     "Mercedes-Benz",
    "BMW":      "BMW",
    "아우디":   "Audi",
    "도요타":   "Toyota",
    "현대":     "Hyundai",
    "기아":     "Kia",
    "제네시스": "Genesis",
    "혼다":     "Honda",
    "지프":     "Jeep",
    "폭스바겐": "Volkswagen",
    "렉서스":   "Lexus",
    "볼보":     "Volvo",
    "포르쉐":   "Porsche",
    "랜드로버": "Land Rover",
    "재규어":   "Jaguar",
    "닛산":     "Nissan",
    "인피니티": "Infiniti",
    "미니":     "MINI",
    "포드":     "Ford",
    "쉐보레":   "Chevrolet",
    "캐딜락":   "Cadillac",
}

ENCAR_API       = "https://api.encar.com/search/car/list/general"
FRANKFURTER_API = "https://api.frankfurter.dev/v1/latest?base=EUR&symbols=KRW"
WEBSITE_TAX_KRW = 440_000  # Encar website tax added to every listing

CARS_JSON = os.path.join(os.path.dirname(__file__), "..", "cars.json")
# ---------------------------------------------------------------------------


def get_exchange_rate() -> float:
    res = requests.get(FRANKFURTER_API, timeout=10)
    res.raise_for_status()
    return res.json()["rates"]["KRW"]


def calc_turnkey(krw: int, krw_per_eur: float) -> int:
    car_eur  = (krw + WEBSITE_TAX_KRW) / krw_per_eur
    tax_base = car_eur + 262.5 + 1700 + 30 + 150
    total    = tax_base * 1.32 + 650
    return round(total / 10) * 10  # round to nearest 10 €


def format_price(eur: int) -> str:
    # e.g. 19930 → "19 930 €"
    return f"{eur:,} €".replace(",", " ")  # non-breaking space


def build_query() -> str:
    cfg = SEARCH_CONFIG
    return (
        f"(And.Hidden.N."
        f"_.CarType.Y."
        f"_.PriceRange.{cfg['min_price_man']}to{cfg['max_price_man']}."
        f"_.MileageRange.0to{cfg['max_mileage']}."
        f"_.YearRange.{cfg['min_year']}to."
        f")"
    )


def fetch_listings() -> list:
    params = {
        "count": "true",
        "q":     build_query(),
        "sr":    f"|ModifiedDate|0|{SEARCH_CONFIG['fetch_count']}",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; CarBot/1.0)",
        "Referer":    "https://www.encar.com/",
        "Accept":     "application/json",
    }
    res = requests.get(ENCAR_API, params=params, headers=headers, timeout=20)
    res.raise_for_status()
    data = res.json()
    return data.get("SearchResults", [])


def photo_url(item: dict) -> str:
    photos = item.get("Photos", [])
    if not photos:
        return ""
    loc = photos[0].get("location", "")
    return (
        f"https://ci.encar.com/{loc}"
        f"?impolicy=heightRate&rh=768&cw=1280&ch=768&cg=Center"
        f"&wtmk=https://ci.encar.com/wt_mark/w_mark_04.png"
    )


def encar_id_from_url(url: str) -> str | None:
    m = re.search(r"/detail/(\d+)", url)
    return m.group(1) if m else None


def load_existing() -> list:
    if not os.path.exists(CARS_JSON):
        return []
    with open(CARS_JSON, encoding="utf-8") as f:
        return json.load(f)


def save(cars: list) -> None:
    with open(CARS_JSON, "w", encoding="utf-8") as f:
        json.dump(cars, f, ensure_ascii=False, indent=2)


def main() -> None:
    print("Fetching exchange rate...")
    rate = get_exchange_rate()
    print(f"  1 EUR = {rate:,.0f} KRW")

    print("Fetching Encar listings...")
    listings = fetch_listings()
    print(f"  {len(listings)} listings returned")

    existing = load_existing()
    known_ids = set()
    for c in existing:
        eid = encar_id_from_url(c.get("encarUrl", ""))
        if eid:
            known_ids.add(eid)

    next_id = max((c.get("id", 0) for c in existing), default=0) + 1
    added = []

    for item in listings:
        car_id = str(item.get("Id", ""))
        if not car_id or car_id in known_ids:
            continue

        price_man = item.get("Price", 0)   # 만원
        krw       = price_man * 10_000
        turnkey   = calc_turnkey(krw, rate)

        raw_brand = item.get("Manufacturer", "")
        brand     = BRAND_MAP.get(raw_brand, raw_brand)
        model     = item.get("Model", "").strip()
        badge     = item.get("Badge", "").strip()
        year      = item.get("Year", "")

        model_str = f"{model} {badge} ({year})".strip()

        new_car = {
            "id":       next_id,
            "brand":    brand,
            "model":    model_str,
            "price":    format_price(turnkey),
            "image":    photo_url(item),
            "encarUrl": f"https://fem.encar.com/cars/detail/{car_id}",
        }
        added.append(new_car)
        known_ids.add(car_id)
        next_id += 1
        print(f"  + {brand} {model_str} — {format_price(turnkey)}")

    if added:
        save(existing + added)
        print(f"\nDone. Added {len(added)} new car(s) to cars.json.")
    else:
        print("\nNo new listings found.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
