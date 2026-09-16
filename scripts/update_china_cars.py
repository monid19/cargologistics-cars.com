"""
Auto-updates china-cars.json with new listings from Guazi.com (Chinese used car marketplace).
- Removes sold/unavailable listings automatically
- Keeps the site capped at MAX_CARS listings
- Runs daily via GitHub Actions
Note: Guazi.com may rate-limit non-CN IPs. The script fails gracefully —
      existing listings are preserved on any network error.
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
MAX_CARS = 8

# Target brands and their English names
TARGET_BRANDS = {
    "比亚迪": "BYD",
    "蔚来":   "NIO",
    "小鹏":   "Xpeng",
    "理想":   "Li Auto",
    "埃安":   "AION",
    "奇瑞":   "Chery",
    "MG":     "MG",
    "名爵":   "MG",
    "吉利":   "Geely",
    "长安":   "Changan",
    "哪吒":   "Neta",
    "问界":   "AITO",
    "极氪":   "Zeekr",
    "岚图":   "Voyah",
}

SEARCH_CONFIG = {
    "min_price_wan": 5,    # 万元 ~6 000 €
    "max_price_wan": 60,   # 万元 ~73 000 €
    "min_year":      2020,
    "max_mileage":   100000,
    "fetch_count":   60,
}

FRANKFURTER_API = "https://api.frankfurter.dev/v1/latest?base=EUR&symbols=CNY"
CHINA_CARS_JSON = os.path.join(os.path.dirname(__file__), "..", "china-cars.json")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept":          "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer":         "https://www.guazi.com/",
}

# Guazi search endpoint — returns JSON paginated results
GUAZI_SEARCH = "https://www.guazi.com/pc/buy"
GUAZI_CHECK  = "https://www.guazi.com/pc/detail"

# ---------------------------------------------------------------------------


def get_exchange_rate() -> float:
    res = requests.get(FRANKFURTER_API, timeout=10)
    res.raise_for_status()
    return res.json()["rates"]["CNY"]


def calc_import_price(cny: float, cny_per_eur: float) -> int:
    """
    Rough landed cost estimate for importing a Chinese car to Bulgaria:
      - Car price in EUR
      - ~1 000 € shipping (China → BG)
      - ~200 € inspection / paperwork
      - Bulgarian import duty 6.5% of car value
      - VAT 20% on (car + duty + shipping)
      - Registration 150 €
    """
    car_eur   = cny / cny_per_eur
    shipping  = 1000
    papers    = 200
    duty      = car_eur * 0.065
    vat_base  = car_eur + duty + shipping + papers
    vat       = vat_base * 0.20
    total     = vat_base + vat + 150
    return round(total / 10) * 10


def format_price(eur: int) -> str:
    return f"{eur:,} €".replace(",", " ")


def load_existing() -> list:
    if not os.path.exists(CHINA_CARS_JSON):
        return []
    with open(CHINA_CARS_JSON, encoding="utf-8") as f:
        return json.load(f)


def save(cars: list) -> None:
    with open(CHINA_CARS_JSON, "w", encoding="utf-8") as f:
        json.dump(cars, f, ensure_ascii=False, indent=2)


def fetch_listings() -> list:
    """
    Queries Guazi.com for used Chinese EVs/new-energy vehicles.
    Returns parsed listing dicts, or empty list on failure.
    """
    cfg = SEARCH_CONFIG
    results = []

    for brand_cn, brand_en in TARGET_BRANDS.items():
        if len(results) >= cfg["fetch_count"]:
            break
        try:
            params = {
                "kw":       brand_cn,
                "pricemin": cfg["min_price_wan"],
                "pricemax": cfg["max_price_wan"],
                "minyear":  cfg["min_year"],
                "page":     1,
            }
            res = requests.get(GUAZI_SEARCH, params=params, headers=HEADERS, timeout=15)
            if res.status_code != 200:
                print(f"  [{brand_en}] HTTP {res.status_code} — skipping")
                continue

            data = res.json()
            items = data.get("data", {}).get("carList", [])
            if not items:
                # Try alternate key structures
                items = data.get("result", data.get("list", []))

            if not items:
                print(f"  [{brand_en}] No listings found or unexpected response format")
                continue

            for item in items:
                mileage = item.get("mileage_num", item.get("kilometer", 999999))
                year    = item.get("year_num",    item.get("year", 0))
                price_w = item.get("display_price", item.get("price", 0))
                try:
                    price_w = float(str(price_w).replace("万", "").strip())
                except (ValueError, AttributeError):
                    price_w = 0

                if (price_w < cfg["min_price_wan"]
                        or price_w > cfg["max_price_wan"]
                        or mileage > cfg["max_mileage"]
                        or year < cfg["min_year"]):
                    continue

                item["_brand_en"] = brand_en
                results.append(item)

            time.sleep(1.0)

        except Exception as exc:
            print(f"  [{brand_en}] Error: {exc}")
            continue

    return results


def is_still_listed(source_url: str) -> bool:
    """Check if a listing page still returns 200. Fail-safe: True on any error."""
    if not source_url or source_url in ("https://en.guazi.com", "https://www.autocango.com"):
        return True  # placeholder entries — keep
    try:
        res = requests.head(source_url, headers=HEADERS, timeout=10, allow_redirects=True)
        return res.status_code < 400
    except Exception:
        return True


def extract_listing(item: dict, new_id: int, cny_per_eur: float) -> dict:
    brand = item.get("_brand_en", "")
    model = (item.get("car_name", "") or item.get("name", "")).strip()
    # Strip brand name from model if duplicated
    if model.startswith(brand):
        model = model[len(brand):].strip()

    year      = item.get("year_num", item.get("year", ""))
    model_str = f"{model} ({year})" if year else model

    price_w   = item.get("display_price", item.get("price", 0))
    try:
        price_w = float(str(price_w).replace("万", "").strip())
    except (ValueError, AttributeError):
        price_w = 0
    cny       = price_w * 10_000
    price_eur = calc_import_price(cny, cny_per_eur) if cny > 0 else 0
    price_str = format_price(price_eur) if price_eur > 0 else "Скоро"

    # Image: prefer first photo
    image = ""
    photos = item.get("pic_url", item.get("photo", item.get("images", [])))
    if isinstance(photos, list) and photos:
        image = photos[0]
    elif isinstance(photos, str) and photos:
        image = photos

    # Listing URL
    car_id     = item.get("carid", item.get("id", ""))
    source_url = f"https://www.guazi.com/pc/detail/{car_id}" if car_id else "https://en.guazi.com"

    return {
        "id":        new_id,
        "brand":     brand,
        "model":     model_str,
        "price":     price_str,
        "image":     image,
        "sourceUrl": source_url,
    }


def main() -> None:
    print("--- Cargo Logistics China car listing updater ---\n")

    print("Fetching EUR/CNY exchange rate...")
    try:
        rate = get_exchange_rate()
        print(f"  1 EUR = {rate:.2f} CNY\n")
    except Exception as exc:
        print(f"  Exchange rate fetch failed: {exc}")
        print("  Using fallback rate 7.8 CNY/EUR")
        rate = 7.8

    existing = load_existing()
    print(f"Checking {len(existing)} existing listing(s) for availability...")
    active = []
    for car in existing:
        url = car.get("sourceUrl", "")
        if is_still_listed(url):
            active.append(car)
            print(f"  [OK]    {car['brand']} {car['model']}")
        else:
            print(f"  [GONE]  {car['brand']} {car['model']} — removed")
        time.sleep(0.3)

    slots = MAX_CARS - len(active)
    print(f"\n{len(active)} active. {slots} slot(s) free (cap: {MAX_CARS}).\n")

    if slots <= 0:
        print("At capacity — no new listings needed.")
        if len(active) != len(existing):
            save(active)
        return

    print("Fetching new listings from Guazi.com...")
    raw = fetch_listings()
    print(f"  {len(raw)} listing(s) matched filters\n")

    known_urls = {c.get("sourceUrl", "") for c in active}
    added = []

    for item in raw:
        if len(added) >= slots:
            break
        car_id = item.get("carid", item.get("id", ""))
        url    = f"https://www.guazi.com/pc/detail/{car_id}" if car_id else ""
        if not url or url in known_urls:
            continue

        entry = extract_listing(item, len(active) + len(added) + 1, rate)
        added.append(entry)
        known_urls.add(url)
        print(f"  [NEW]   {entry['brand']} {entry['model']} — {entry['price']}")

    final = active + added
    save(final)
    print(f"\nDone. {len(added)} added, {len(existing) - len(active)} removed. "
          f"Total: {len(final)}/{MAX_CARS}.")


if __name__ == "__main__":
    main()
