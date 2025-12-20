import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import random
import os
import pytz  # Indian timezone

# ----------------------------
# 1. PRODUCT LIST
# ----------------------------
URLS = [
    "https://amzn.in/d/bqE35ja", "https://amzn.in/d/8DkcqwJ", "https://amzn.in/d/27dBhA1",
    "https://amzn.in/d/5fRuGGr", "https://amzn.in/d/i9MHRbf", "https://amzn.in/d/4mstrat",
    "https://amzn.in/d/8D9SlMj", "https://amzn.in/d/0V4kPll", "https://amzn.in/d/bGuw5EZ",
    "https://amzn.in/d/aNPi1U2", "https://amzn.in/d/isCQv09", "https://amzn.in/d/7mqmyMs",
    "https://amzn.in/d/axvUrmf", "https://amzn.in/d/0D9RJyQ", "https://amzn.in/d/iUJnAAG",
    "https://amzn.in/d/fCdbdzb", "https://amzn.in/d/fGRPZHm", "https://amzn.in/d/d8JD7Ef",
    "https://amzn.in/d/9Vmpx9L", "https://amzn.in/d/1yTk7TG", "https://amzn.in/d/amDxu6e",
    "https://amzn.in/d/8MCAq5Z", "https://amzn.in/d/8Xctx1i", "https://amzn.in/d/fETFYB9",
    "https://amzn.in/d/eQdsGNY"
]

# ----------------------------
# 2. USER AGENTS (25)
# ----------------------------
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_6_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_7_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_7_10) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",

    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.193 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.90 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-A505F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.132 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 9; Redmi Note 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.92 Mobile Safari/537.36",

    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",

    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.140 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.149 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.5993.88 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]

# ----------------------------
# REFERERS
# ----------------------------
REFERERS = [
    "https://www.google.com/",
    "https://www.amazon.in/",
    "https://www.bing.com/"
]

# ----------------------------
# CONFIG
# ----------------------------
FILENAME = "price_tracker_final.xlsx"
IST = pytz.timezone("Asia/Kolkata")

# ----------------------------
# ENSURE EXCEL EXISTS
# ----------------------------
def ensure_excel_file():
    if not os.path.exists(FILENAME):
        df = pd.DataFrame(columns=["SKU Name"])
        with pd.ExcelWriter(FILENAME, engine="openpyxl", mode="w") as writer:
            df.to_excel(writer, index=False)
        print("📄 Excel file created for first run.")

# ----------------------------
# AMAZON SCRAPER
# ----------------------------
def get_amazon_data(url):
    for _ in range(3):
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept-Language": "en-IN,en-GB,en;q=0.9",
                "Referer": random.choice(REFERERS),
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive"
            }

            time.sleep(random.uniform(12, 25))
            response = requests.get(url, headers=headers, timeout=30)

            if response.status_code != 200:
                continue

            if "automated access" in response.text.lower():
                print(f"⚠️ Blocked: {url}")
                continue

            soup = BeautifulSoup(response.content, "html.parser")

            title_tag = soup.find("span", {"id": "productTitle"})
            price_tag = soup.select_one(".a-price-whole") or soup.select_one(".apexPriceToPay .a-offscreen")

            if not title_tag or not price_tag:
                continue

            title = title_tag.get_text(strip=True)
            price_raw = price_tag.get_text().replace(",", "").replace("₹", "").strip()
            price = int("".join(filter(str.isdigit, price_raw)))

            return {"Product": title, "Price": price}

        except Exception:
            continue

    return None

# ----------------------------
# TRACKER
# ----------------------------
def run_price_tracker():
    run_time = datetime.now(IST).strftime("%Y-%m-%d %H:%M")

    if os.path.exists(FILENAME):
        df = pd.read_excel(FILENAME)
    else:
        df = pd.DataFrame(columns=["SKU Name"])

    if "SKU Name" not in df.columns:
        df.insert(0, "SKU Name", "")

    df.insert(1, run_time, "")
    random.shuffle(URLS)

    for i, url in enumerate(URLS, 1):
        print(f"[{i}/{len(URLS)}] Checking product...")
        data = get_amazon_data(url)
        if not data:
            continue

        sku = data["Product"]
        price = data["Price"]

        if sku in df["SKU Name"].values:
            df.loc[df["SKU Name"] == sku, run_time] = price
        else:
            row = {col: "" for col in df.columns}
            row["SKU Name"] = sku
            row[run_time] = price
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

    with pd.ExcelWriter(FILENAME, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, index=False)
        ws = writer.sheets["Sheet1"]
        for col in ws.columns:
            width = max(len(str(cell.value)) if cell.value else 0 for cell in col)
            ws.column_dimensions[col[0].column_letter].width = width + 5

    print("✅ Latest price inserted first. Older prices shifted right.")

# ----------------------------
# RUN
# ----------------------------
if __name__ == "__main__":
    ensure_excel_file()
    while True:
        run_price_tracker()
        print("⏰ Waiting 1 hour before next fetch...")
        time.sleep(3600)
