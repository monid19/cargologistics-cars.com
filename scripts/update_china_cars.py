"""
Auto-updates china-cars.json with listings from autocango.com.
Uses Playwright headless browser (required — site uses JS rendering).
Runs daily via GitHub Actions (self-hosted runner with Playwright installed).
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
    sys.exit(0)

import requests

# ---------------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------------
MAX_CARS = 8

# (display name, autocango brandName URL param)
BRANDS = [
    ("BYD",     "BYD"),
    ("NIO",     "NIO"),
    ("XPeng",   "XPeng"),
    ("Chery",   "Chery"),
    ("MG",      "MG"),
    ("Geely",   "Geely"),
    ("Li Auto", "Li Auto"),
    ("AION",    "Aion"),
]

MIN_YEAR    = 2020
MAX_MILEAGE = 100_000   # km
MIN_FOB_USD = 5_000
MAX_FOB_USD = 80_000
SKIP_CONDITIONS = {"minor accident", "major accident", "flood", "fire", "salvage"}

FRANKFURTER_API = "https://api.frankfurter.dev/v1/latest?base=EUR&symbols=USD"
CHINA_CARS_JSON = os.path.join(os.path.dirname(__file__), "..", "china-cars.json")
BASE_URL        = "https://www.autocango.com"

BROWSER_ARGS = [
    "--disable-blink-features=AutomationControlled",
    "--no-sandbox",
]

CONTEXT_KWARGS = dict(
    user_agent=(
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    locale="en-US",
    viewport={"width": 1280, "height": 800},
    extra_http_headers={
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "sec-ch-ua": '"Chromium";v="124", "Google Chrome";v="124"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    },
)

STEALTH_SCRIPT = """
    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
    window.chrome = {runtime: {}};
"""

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


def parse_card(card_text: str, card_href: str, card_img: str, brand_name: str) -> dict | None:
    """
    Card text structure (double-newline separated):
      0: city | 1: SKU | 2: "YEAR BRAND MODEL ENGINE..."
      3: "Reg. Year" | 4: reg-date | 5: "Mlg(km)" | 6: mileage
      7: "Fuel" | 8: fuel-type | ... (specs table) ... | N: "$price"
    Uses regex on the full text rather than fragile index lookups.
    """
    parts = [p.strip() for p in card_text.split("\n\n") if p.strip()]
    if len(parts) < 5:
        return None

    # Title is always parts[2]
    title = parts[2]
    year_match = re.match(r'^(20\d{2})\s+', title)
    if not year_match:
        return None
    year = int(year_match.group(1))
    if year < MIN_YEAR:
        return None

    # Mileage: labelled "Mlg(km)" followed by the number
    mileage_match = re.search(r'Mlg\(km\)\n\n(\d+)', card_text)
    mileage = int(mileage_match.group(1)) if mileage_match else 0
    if mileage > MAX_MILEAGE:
        return None

    # Price: find first $N,NNN in the text (FOB price)
    prices = [int(m.replace(',', '')) for m in re.findall(r'\$([0-9,]+)', card_text)]
    fob_usd = next((p for p in prices if MIN_FOB_USD <= p <= MAX_FOB_USD), 0)
    if not fob_usd:
        return None

    # Skip damaged cars (condition block appears before the spec table)
    condition_block = card_text.split("\n\nModel Year")[0].lower() if "\n\nModel Year" in card_text else card_text.lower()
    if any(s in condition_block for s in SKIP_CONDITIONS):
        return None

    # Model: strip year + brand prefix, then clean engine specs
    model = re.sub(rf'^{year}\s+{re.escape(brand_name)}\s*', '', title, flags=re.IGNORECASE).strip()
    model = re.sub(r'\s+\d+\.\d+[LT].*$', '', model).strip()

    return {
        "brand":     brand_name,
        "model":     f"{model} ({year})",
        "fob_usd":   fob_usd,
        "image":     card_img or "",
        "sourceUrl": card_href,
    }


def scrape_brand(page, brand_name: str, brand_slug: str, known_urls: set, slots: int) -> list:
    url = f"{BASE_URL}/usedcar/brandName={brand_slug}"
    print(f"  Opening {url}...")

    try:
        page.goto(url, timeout=30_000, wait_until="domcontentloaded")
        page.wait_for_selector('a[href*="/sku/"]', timeout=20_000)
    except PWTimeout:
        print(f"  Timeout / no listings for {brand_name} — skipping")
        return []

    for _ in range(3):
        page.evaluate("window.scrollBy(0, 800)")
        time.sleep(0.4)

    cards = page.eval_on_selector_all(
        'a[href*="/sku/"]',
        """els => els.map(a => ({
            href: a.href,
            text: a.innerText,
            img:  (a.querySelector('img') || {}).src || ''
        }))"""
    )

    print(f"  Found {len(cards)} listing(s) for {brand_name}")
    added = []
    for card in cards:
        if len(added) >= slots:
            break
        if card["href"] in known_urls:
            continue
        entry = parse_card(card["text"], card["href"], card["img"], brand_name)
        if entry is None:
            continue
        added.append(entry)
        known_urls.add(card["href"])
        print(f"    [NEW] {brand_name} {entry['model']} — ${entry['fob_usd']}")

    return added


USD_PER_EUR = 1.08  # fallback, overwritten in main()


def main() -> None:
    global USD_PER_EUR

    print("--- Cargo Logistics China car listing updater (autocango.com) ---\n")

    print("Fetching USD/EUR rate...")
    try:
        USD_PER_EUR = get_exchange_rate()
        print(f"  1 EUR = {USD_PER_EUR:.4f} USD\n")
    except Exception as exc:
        print(f"  Rate fetch failed ({exc}) — using fallback 1.08\n")

    existing = load_existing()
    placeholders = [c for c in existing if c.get("placeholder")]
    # Drop stale real listings — replace catalog each run like the Korea script
    print(f"Replacing {len([c for c in existing if not c.get('placeholder')])} existing listing(s).\n")

    known_urls: set = set()
    all_new = []

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, args=BROWSER_ARGS)
        ctx = browser.new_context(**CONTEXT_KWARGS)
        page = ctx.new_page()
        page.add_init_script(STEALTH_SCRIPT)

        for brand_name, brand_slug in BRANDS:
            if len(all_new) >= MAX_CARS:
                break
            remaining = MAX_CARS - len(all_new)
            print(f"\n[{brand_name}]")
            new_entries = scrape_brand(page, brand_name, brand_slug, known_urls, remaining)
            all_new.extend(new_entries)
            if new_entries:
                time.sleep(1.5)

        ctx.close()
        browser.close()

    # Guard: if scraping returned nothing, keep existing catalog
    if not all_new:
        print("\nNo results scraped — keeping existing china-cars.json unchanged.")
        return

    # Convert prices
    for entry in all_new:
        fob_usd = entry.pop("fob_usd")
        entry["price"] = format_price(calc_import_price(fob_usd, USD_PER_EUR))

    real_count = len(all_new)
    remaining_placeholders = placeholders[:max(0, MAX_CARS - real_count)]
    final = all_new + remaining_placeholders
    for i, car in enumerate(final):
        car["id"] = i + 1

    save(final)
    print(f"\nDone. {real_count} real listing(s) saved. Total: {len(final)}/{MAX_CARS}")


if __name__ == "__main__":
    main()
