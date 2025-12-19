import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import random
import os

# 1. PRODUCT LIST
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

# 2. 25+ HIGH-QUALITY USER AGENTS (Windows, Mac, Linux, iOS, Android)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
    "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 OPR/114.0.0.0",
    "Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:132.0) Gecko/20100101 Firefox/132.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Vivaldi/6.9.3447.37",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/131.0.6778.85 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Linux i686; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
]

REFERERS = [
    "https://www.google.com/", "https://www.bing.com/", 
    "https://duckduckgo.com/", "https://www.amazon.in/"
]

FILENAME = "price_tracker_final.xlsx"

def get_amazon_data(url):
    for attempt in range(3):
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept-Language": "en-IN,en-GB,en;q=0.9",
                "Referer": random.choice(REFERERS),
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive"
            }
            # Mandatory random delay (12-25 seconds) to look human
            time.sleep(random.uniform(12, 25))
            
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code != 200: continue
            
            # Check for CAPTCHA/Block
            if "automated access" in response.text.lower():
                print(f"Blocked on {url}. Retrying...")
                continue

            soup = BeautifulSoup(response.content, "html.parser")
            title = soup.find("span", {"id": "productTitle"}).get_text().strip()
            price_tag = soup.select_one(".a-price-whole") or soup.select_one(".apexPriceToPay .a-offscreen")
            
            if price_tag:
                price_raw = price_tag.get_text().replace(",", "").replace("₹", "").strip()
                price = int("".join(filter(str.isdigit, price_raw.split('.')[0])))
                return {"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "Product": title, "Price": price, "URL": url}
        except: continue
    return None

def get_status(new_entry, df_old):
    if df_old is None or df_old.empty: return "Initial Entry"
    try:
        prev = df_old[df_old['URL'] == new_entry['URL']]
        if not prev.empty:
            last_p = prev.iloc[0]['Price']
            diff = new_entry['Price'] - int(last_p)
            if diff < 0: return f"🔻 DROP (By ₹{abs(diff)})"
            elif diff > 0: return f"🔺 UP (By ₹{diff})"
            else: return "Stable"
    except: pass
    return "New Record"

if __name__ == "__main__":

    run_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Read existing Excel (do not change file name)
    if os.path.exists(FILENAME):
        df = pd.read_excel(FILENAME)
    else:
        df = pd.DataFrame(columns=["SKU Name"])

    # Ensure SKU Name column exists
    if "SKU Name" not in df.columns:
        df.insert(0, "SKU Name", "")

    # 🔥 INSERT LATEST PRICE COLUMN FIRST (Column B)
    df.insert(1, run_time, "")

    # Shuffle URLs (existing behavior kept)
    random.shuffle(URLS)

    for i, url in enumerate(URLS):
        print(f"[{i+1}/{len(URLS)}] Checking product...")
        data = get_amazon_data(url)

        if not data:
            continue

        sku = data["Product"]
        price = data["Price"]

        # If SKU already exists → update price
        if sku in df["SKU Name"].values:
            df.loc[df["SKU Name"] == sku, run_time] = price
        else:
            # New SKU → add row (do not disturb existing columns)
            new_row = {col: "" for col in df.columns}
            new_row["SKU Name"] = sku
            new_row[run_time] = price
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Save back to same Excel
    df.to_excel(FILENAME, index=False)

    print("✅ Latest price inserted first. Older prices shifted right.")
