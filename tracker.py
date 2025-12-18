import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import random
import os

# 1. 25 PRODUCT LINKS
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

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
]

FILENAME = "price_tracker_final.xlsx"

def get_amazon_data(url):
    for attempt in range(3):
        try:
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept-Language": "en-IN,en-GB,en;q=0.9",
                "Referer": "https://www.google.com/"
            }
            # Mandatory delay to avoid IP blocking
            time.sleep(random.uniform(10, 20))
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code != 200: continue

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
    df_old = pd.read_excel(FILENAME) if os.path.exists(FILENAME) else None
    batch = []
    
    # Shuffle URLs to act like a human
    random.shuffle(URLS)

    for i, url in enumerate(URLS):
        print(f"Checking {i+1}/25...")
        data = get_amazon_data(url)
        if data:
            data["Price Change"] = get_status(data, df_old)
            batch.append(data)

    if batch:
        df_new = pd.DataFrame(batch)
        # Combine: New scan at the TOP
        df_final = pd.concat([df_new, df_old], ignore_index=True) if df_old is not None else df_new
        df_final.to_excel(FILENAME, index=False)
        print("Success.")
