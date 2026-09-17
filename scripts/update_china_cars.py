"""
Auto-updates china-cars.json with listings from en.guazi.com.
Uses Playwright headless browser (required — the site is a JS SPA).
Runs daily via GitHub Actions.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout
except ImportError:
    print("Playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(0)  # Exit cleanly so workflow doesn't fail on missing dep

import requests

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------
MAX_CARS = 8

BRANDS = [
    ("BYD",    "byd"),
    ("NIO",    "nio"),
    ("Xpeng",  "xpeng"),
    ("Chery",  "chery"),
    ("MG",     "mg"),
    ("Geely",  "geely-auto"),
    ("Li Auto","lixiang"),
    ("AION",   "aion"),
]

MIN_YEAR    = 2020
MAX_MILEAGE = 100_000   # km
MIN_FOB_USD = 5_000
MAX_FOB_USD = 80_000

FRANKFURTER_API = "https://api.frankfurter.dev/v1/latest?base=EUR&symbols=USD"
CHINA_CARS_JSON = os.path.join(os.path.dirname(__file__), "..", "china-cars.json")
BASE_URL        = "https://en.guazi.com"

# ---------------------------------------------------------------------------


def get_exchange_rate() -> float:
    res = requests.get(FRANKFURTER_API, timeout=10)
    res.raise_for_status()
    return res.json()["rates"]["USD"]


def calc_import_price(fob_usd: float, usd_per_eur: float) -> int:
    fob_eur  = fob_usd / usd_per_eur
    shipping = 1200
    papers   = 250
    duty     = (fob_eur + shipping) * 0.065
    vat_base = fob_eur + shipping + papers + duty
    vat      = vat_base * 0.20
    total    = vat_base + vat + 150
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


CONTEXT_KWARGS = dict(
    user_agent=(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    locale="en-US",
)


def fetch_product_page(browser, product_url: str, brand_name: str) -> dict | None:
    """Open a fresh browser context for each product page to avoid rate-limiting."""
    ctx = browser.new_context(**CONTEXT_KWARGS)
    try:
        page = ctx.new_page()
        try:
            page.goto(product_url, timeout=30_000, wait_until="domcontentloaded")
            page.wait_for_function("document.title.length > 10", timeout=12_000)
            time.sleep(1.5)
        except PWTimeout:
            return None

        title = page.title()
        # Security verification page — blocked
        if "security" in title.lower() or "verification" in title.lower():
            return None

        title = re.sub(r'\s+for\s+Sale.*', '', title, flags=re.IGNORECASE).strip()
        title = re.sub(r'^Used\s+', '', title, flags=re.IGNORECASE).strip()
        model = re.sub(rf'^{re.escape(brand_name)}\s+', '', title, flags=re.IGNORECASE).strip()

        year_match = re.search(r'\b(20\d{2})\b', model)
        year = int(year_match.group(1)) if year_match else 0
        if year < MIN_YEAR:
            return None

        body_text = page.inner_text('body')
        price_matches = re.findall(r'\$([0-9,]+)', body_text)
        fob_usd = 0
        for pm in price_matches:
            try:
                val = int(pm.replace(',', ''))
                if MIN_FOB_USD <= val <= MAX_FOB_USD:
                    fob_usd = val
                    break
            except ValueError:
                pass
        if fob_usd == 0:
            return None

        image = page.eval_on_selector_all(
            'img',
            "els => els.map(i => i.src).find(s => s.includes('guazistatic-global.com')) || ''"
        ) or ""

        return {"model": model, "fob_usd": fob_usd, "image": image}
    finally:
        ctx.close()


def scrape_brand_listings(browser, brand_name: str, brand_slug: str,
                          known_urls: set, slots: int) -> list:
    """Navigate to a brand listing page and extract car entries."""
    url = f"{BASE_URL}/used-cars/{brand_slug}/"
    print(f"  Opening {url}...")

    ctx = browser.new_context(**CONTEXT_KWARGS)
    try:
        page = ctx.new_page()
        try:
            page.goto(url, timeout=30_000, wait_until="domcontentloaded")
            page.wait_for_selector('a[href*="/products/"]', timeout=20_000)
        except PWTimeout:
            print(f"  Timeout / no product links for {url} — skipping")
            return []

        for _ in range(3):
            page.evaluate("window.scrollBy(0, 800)")
            time.sleep(0.5)

        links = page.eval_on_selector_all(
            'a[href*="/products/"]',
            'els => [...new Set(els.map(a => a.href))]'
        )
    finally:
        ctx.close()

    print(f"  Found {len(links)} product URLs")

    added = []
    for product_url in links:
        if len(added) >= slots:
            break
        if product_url in known_urls:
            continue

        mileage_match = re.search(r'-(\d+)km-', product_url)
        if mileage_match and int(mileage_match.group(1)) > MAX_MILEAGE:
            continue

        print(f"    Fetching {product_url.split('/')[-1][:60]}...")
        data = fetch_product_page(browser, product_url, brand_name)
        if data is None:
            time.sleep(2)
            continue

        eur_price = calc_import_price(data["fob_usd"], USD_PER_EUR)
        entry = {
            "id":        -1,
            "brand":     brand_name,
            "model":     data["model"],
            "price":     format_price(eur_price),
            "image":     data["image"],
            "sourceUrl": product_url,
        }
        added.append(entry)
        known_urls.add(product_url)
        print(f"    [NEW] {brand_name} {data['model']} — {format_price(eur_price)}")
        time.sleep(2)

    return added


USD_PER_EUR = 1.08  # fallback, overwritten in main()


def is_still_listed(url: str) -> bool:
    if not url or url in ("https://en.guazi.com", "https://www.autocango.com"):
        return True
    try:
        res = requests.head(url, timeout=10, allow_redirects=True)
        return res.status_code < 400
    except Exception:
        return True


def main() -> None:
    global USD_PER_EUR

    print("--- Cargo Logistics China car listing updater (en.guazi.com) ---\n")

    print("Fetching USD/EUR rate...")
    try:
        USD_PER_EUR = get_exchange_rate()
        print(f"  1 EUR = {USD_PER_EUR:.4f} USD\n")
    except Exception as exc:
        print(f"  Rate fetch failed ({exc}) — using fallback 1.08\n")

    existing = load_existing()
    print(f"Checking {len(existing)} existing listing(s)...")
    placeholders = []
    active = []
    for car in existing:
        if car.get("placeholder"):
            placeholders.append(car)
            continue
        url = car.get("sourceUrl", "")
        if is_still_listed(url):
            active.append(car)
            print(f"  [OK]    {car['brand']} {car['model']}")
        else:
            print(f"  [GONE]  {car['brand']} {car['model']} — removed")
        time.sleep(0.3)

    # Placeholders count as free slots
    slots = MAX_CARS - len(active)
    print(f"\n{len(active)} real listing(s), {len(placeholders)} placeholder(s). "
          f"{slots} slot(s) free (cap: {MAX_CARS}).\n")

    if slots <= 0:
        print("At capacity with real listings — no scraping needed.")
        save(active)
        return

    known_urls = {c.get("sourceUrl", "") for c in active}
    all_new = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)

        for brand_name, brand_slug in BRANDS:
            if len(all_new) >= slots:
                break
            remaining = slots - len(all_new)
            print(f"\n[{brand_name}]")
            new_entries = scrape_brand_listings(browser, brand_name, brand_slug,
                                               known_urls, remaining)
            all_new.extend(new_entries)

        browser.close()

    # Real listings first, then fill remaining slots with placeholders
    real_count = len(active) + len(all_new)
    remaining_placeholders = placeholders[: max(0, MAX_CARS - real_count)]

    final = active + all_new + remaining_placeholders
    for i, car in enumerate(final):
        car["id"] = i + 1

    save(final)
    removed = len(existing) - len(active) - len(placeholders)
    print(f"\nDone. {len(all_new)} added, {removed} removed. "
          f"Total: {len(final)}/{MAX_CARS} ({real_count} real, {len(remaining_placeholders)} placeholders).")


if __name__ == "__main__":
    main()
