"""
Auto-updates cars.json with new listings from Encar.
- Removes sold/unavailable listings automatically
- Keeps the site capped at MAX_CARS listings
- Runs daily via GitHub Actions
"""

import json
import os
import re
import sys
import time
import requests

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------
MAX_CARS = 12   # maximum cars shown on the website at any time

SEARCH_CONFIG = {
    "min_price_man": 500,    # 만원 → 500 = 5 000 000 KRW (~2 800 €)
    "max_price_man": 5000,   # 만원 → 5000 = 50 000 000 KRW (~28 000 €)
    "max_mileage":   150000, # km
    "min_year":      2015,
    "fetch_count":   40,     # how many recent Encar listings to scan per run
}

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

ENCAR_API        = "https://api.encar.com/search/car/list/general"
ENCAR_DETAIL_API = "https://api.encar.com/cars/detail/{car_id}"
FRANKFURTER_API  = "https://api.frankfurter.dev/v1/latest?base=EUR&symbols=KRW"
WEBSITE_TAX_KRW  = 440_000

CARS_JSON = os.path.join(os.path.dirname(__file__), "..", "cars.json")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; CarBot/1.0)",
    "Referer":    "https://www.encar.com/",
    "Accept":     "application/json",
}
# ---------------------------------------------------------------------------


def get_exchange_rate() -> float:
    res = requests.get(FRANKFURTER_API, timeout=10)
    res.raise_for_status()
    return res.json()["rates"]["KRW"]


def calc_turnkey(krw: int, krw_per_eur: float) -> int:
    car_eur  = (krw + WEBSITE_TAX_KRW) / krw_per_eur
    tax_base = car_eur + 262.5 + 1700 + 30 + 150
    total    = tax_base * 1.32 + 650
    return round(total / 10) * 10


def format_price(eur: int) -> str:
    return f"{eur:,} €".replace(",", " ")


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


def is_still_active(car_id: str) -> bool:
    """Returns True if the listing is still live on Encar, False if sold/removed."""
    try:
        url = ENCAR_DETAIL_API.format(car_id=car_id)
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 404:
            return False
        if res.status_code == 200:
            data = res.json()
            # Encar marks sold cars with StatusType "sale_close" or similar
            status = data.get("StatusType", "") or data.get("State", "")
            if "close" in str(status).lower() or "sold" in str(status).lower():
                return False
            return True
        return True  # on unexpected status, keep the car (fail safe)
    except Exception:
        return True  # on network error, keep the car (fail safe)


def fetch_new_listings() -> list:
    params = {
        "count": "true",
        "q":     build_query(),
        "sr":    f"|ModifiedDate|0|{SEARCH_CONFIG['fetch_count']}",
    }
    res = requests.get(ENCAR_API, params=params, headers=HEADERS, timeout=20)
    res.raise_for_status()
    return res.json().get("SearchResults", [])


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


def extract_car_id(url: str) -> str | None:
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
    print("--- Cargo Logistics car listing updater ---\n")

    # 1. Exchange rate
    print("Fetching exchange rate...")
    rate = get_exchange_rate()
    print(f"  1 EUR = {rate:,.0f} KRW\n")

    # 2. Check existing cars — remove sold ones
    existing = load_existing()
    print(f"Checking {len(existing)} existing listing(s) for availability...")
    active = []
    for car in existing:
        car_id = extract_car_id(car.get("encarUrl", ""))
        if not car_id:
            active.append(car)
            continue
        if is_still_active(car_id):
            active.append(car)
            print(f"  [OK]     {car['brand']} {car['model']}")
        else:
            print(f"  [SOLD]   {car['brand']} {car['model']} — removed")
        time.sleep(0.3)  # be polite to Encar's servers

    slots_available = MAX_CARS - len(active)
    print(f"\n{len(active)} active listing(s). {slots_available} slot(s) available (cap: {MAX_CARS}).\n")

    if slots_available <= 0:
        print("Site is at capacity. No new listings fetched.")
        if len(active) != len(existing):
            save(active)
            print("Saved updated cars.json (sold cars removed).")
        return

    # 3. Fetch new listings from Encar
    print("Fetching new listings from Encar...")
    raw = fetch_new_listings()
    print(f"  {len(raw)} listings returned from search\n")

    known_ids = {extract_car_id(c.get("encarUrl", "")) for c in active}
    added = []

    for item in raw:
        if len(added) >= slots_available:
            break

        car_id = str(item.get("Id", ""))
        if not car_id or car_id in known_ids:
            continue

        price_man = item.get("Price", 0)
        krw       = price_man * 10_000
        turnkey   = calc_turnkey(krw, rate)

        raw_brand = item.get("Manufacturer", "")
        brand     = BRAND_MAP.get(raw_brand, raw_brand)
        model     = (item.get("Model", "") or "").strip()
        badge     = (item.get("Badge", "") or "").strip()
        year      = item.get("Year", "")
        model_str = f"{model} {badge} ({year})".strip()

        new_car = {
            "id":       len(active) + len(added) + 1,
            "brand":    brand,
            "model":    model_str,
            "price":    format_price(turnkey),
            "image":    photo_url(item),
            "encarUrl": f"https://fem.encar.com/cars/detail/{car_id}",
        }
        added.append(new_car)
        known_ids.add(car_id)
        print(f"  [NEW]    {brand} {model_str} — {format_price(turnkey)}")

    # 4. Save
    final = active + added
    save(final)

    print(f"\nDone. {len(added)} added, {len(existing) - len(active)} removed. "
          f"Total on site: {len(final)}/{MAX_CARS}.")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        sys.exit(1)
