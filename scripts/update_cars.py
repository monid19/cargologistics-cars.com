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
MAX_CARS = 12

SEARCH_CONFIG = {
    "min_price_man": 500,    # 만원 → ~2 800 €
    "max_price_man": 5000,   # 만원 → ~28 000 €
    "max_mileage":   150000,
    "min_year":      2015,
    "fetch_count":   40,
}

MODEL_MAP = {
    # Hyundai
    "아반떼": "Elantra", "쏘나타": "Sonata", "그랜저": "Grandeur",
    "투싼": "Tucson", "싼타페": "Santa Fe", "팰리세이드": "Palisade",
    "더 뉴 팰리세이드": "Palisade", "캐스퍼": "Casper",
    "아이오닉5": "Ioniq 5", "아이오닉6": "Ioniq 6",
    "넥쏘": "Nexo", "코나": "Kona", "베뉴": "Venue",
    "스타렉스": "Staria", "그랜드 스타렉스": "Grand Starex",
    "더 뉴 그랜드 스타렉스": "Grand Starex",
    # Kia
    "K3": "K3", "K5": "K5", "K7": "K7", "K8": "K8", "K9": "K9",
    "스팅어": "Stinger", "카니발": "Carnival", "스포티지": "Sportage",
    "쏘렌토": "Sorento", "더 뉴 쏘렌토": "Sorento",
    "모하비": "Mohave", "셀토스": "Seltos", "니로": "Niro",
    "EV6": "EV6", "EV9": "EV9", "레이": "Ray", "모닝": "Morning",
    # Genesis
    "G70": "G70", "G80": "G80", "G90": "G90",
    "GV70": "GV70", "GV80": "GV80",
    # BMW
    "3시리즈": "3 Series", "5시리즈": "5 Series", "7시리즈": "7 Series",
    "X3": "X3", "X5": "X5", "X6": "X6",
    # Mercedes
    "C클래스": "C-Class", "E클래스": "E-Class", "S클래스": "S-Class",
    "GLC": "GLC", "GLE": "GLE",
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

FRANKFURTER_API = "https://api.frankfurter.dev/v1/latest?base=EUR&symbols=KRW"
WEBSITE_TAX_KRW = 440_000

CARS_JSON = os.path.join(os.path.dirname(__file__), "..", "cars.json")

# Rotate through search endpoints — try each until one works
SEARCH_ENDPOINTS = [
    "https://api.encar.com/search/car/list/general",
    "https://api.encar.com/search/car/list/premium",
]

# Browser-like headers to reduce blocking
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept":          "application/json, text/plain, */*",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer":         "https://www.encar.com/",
    "Origin":          "https://www.encar.com",
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


def is_still_active(car_id: str) -> bool:
    """
    Uses the same search API that works from GitHub Actions.
    Searches for the specific car ID — if Count is 0 it is sold/removed.
    Defaults to True on ANY error (fail-safe — never removes due to network issue).
    """
    try:
        params = {
            "count": "true",
            "q":     f"(And.Hidden.N._.Id.{car_id}.)",
            "sr":    "|ModifiedDate|0|1",
        }
        res = requests.get(SEARCH_ENDPOINTS[0], params=params, headers=HEADERS, timeout=12)
        if res.status_code == 200:
            data  = res.json()
            count = data.get("Count", 1)  # default 1 = keep car if field missing
            return count > 0
    except Exception:
        pass
    return True  # fail-safe


def fetch_new_listings() -> list:
    """
    Tries multiple Encar search endpoints with progressively simpler queries.
    Returns empty list (not an error) if all attempts fail.
    """
    cfg = SEARCH_CONFIG
    queries = [
        "(And.Hidden.N._.CarType.Y.)",   # passenger cars only
        "(And.Hidden.N.)",               # all types (fallback)
    ]

    for endpoint in SEARCH_ENDPOINTS:
        for query in queries:
            try:
                params = {
                    "count": "true",
                    "q":     query,
                    "sr":    f"|ModifiedDate|0|{cfg['fetch_count']}",
                }
                res = requests.get(endpoint, params=params, headers=HEADERS, timeout=20)
                if res.status_code != 200:
                    continue
                results = res.json().get("SearchResults", [])
                if not results:
                    continue

                print(f"  Search succeeded: {endpoint} | query: {query}")

                # Filter in Python — safe regardless of which query worked
                filtered = [
                    item for item in results
                    if (cfg["min_price_man"] <= item.get("Price", 0) <= cfg["max_price_man"]
                        and item.get("Mileage", 0)  <= cfg["max_mileage"]
                        and item.get("Year",    0)  >= cfg["min_year"])
                ]
                return filtered

            except Exception as exc:
                print(f"  Attempt failed ({endpoint}): {exc}")
                continue

    print("  All search attempts failed — no new listings added this run.")
    return []


def photo_url(item: dict) -> str:
    photos = item.get("Photos", [])
    if not photos:
        return ""
    loc = photos[0].get("location", "").lstrip("/")
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

    print("Fetching exchange rate...")
    rate = get_exchange_rate()
    print(f"  1 EUR = {rate:,.0f} KRW\n")

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
            print(f"  [SOLD]   {car['brand']} {car['model']} - removed")
        time.sleep(0.5)

    slots_available = MAX_CARS - len(active)
    print(f"\n{len(active)} active listing(s). {slots_available} slot(s) available (cap: {MAX_CARS}).\n")

    if slots_available <= 0:
        print("Site is at capacity. No new listings needed.")
        if len(active) != len(existing):
            save(active)
        return

    print("Fetching new listings from Encar...")
    raw = fetch_new_listings()
    print(f"  {len(raw)} listing(s) matched filters\n")

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
        raw_model = (item.get("ModelGroup", "") or item.get("Model", "") or "").strip()
        # Try longest-match first in MODEL_MAP for compound Korean names
        model = raw_model
        for k, v in sorted(MODEL_MAP.items(), key=lambda x: -len(x[0])):
            if k in raw_model:
                model = v
                break
        badge     = (item.get("Badge",  "") or "").strip()
        # Year comes as YYYYMM.0 — extract just the 4-digit year
        raw_year  = str(item.get("Year", "") or "")
        year      = raw_year[:4] if len(raw_year) >= 4 else raw_year
        model_str = f"{model} {badge} ({year})".strip() if badge else f"{model} ({year})"

        added.append({
            "id":       len(active) + len(added) + 1,
            "brand":    brand,
            "model":    model_str,
            "price":    format_price(turnkey),
            "image":    photo_url(item),
            "encarUrl": f"https://fem.encar.com/cars/detail/{car_id}",
        })
        known_ids.add(car_id)
        print(f"  [NEW]    {brand} {model_str} - {format_price(turnkey)}")

    final = active + added
    save(final)
    print(f"\nDone. {len(added)} added, {len(existing) - len(active)} removed. "
          f"Total: {len(final)}/{MAX_CARS}.")


if __name__ == "__main__":
    main()  # no sys.exit(1) — always exit cleanly so the workflow succeeds
