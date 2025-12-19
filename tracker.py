import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import time
import random
import os
import pytz  # For Indian timezone

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

# 2. USER AGENTS & REFERERS (unchanged)
USER_AGENTS = [ ... ]  # keep your full list
REFERERS = [ ... ]  # keep your full list

FILENAME = "price_tracker_final.xlsx"
IST = pytz.timezone('Asia/Kolkata')  # Indian Standard Time

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
            time.sleep(random.uniform(12, 25))
            response = requests.get(url, headers=headers, timeout=30)
            if response.status_code != 200: continue
            if "automated access" in response.text.lower():
                print(f"Blocked on {url}. Retrying...")
                continue

            soup = BeautifulSoup(response.content, "html.parser")
            title = soup.find("span", {"id": "productTitle"}).get_text().strip()
            price_tag = soup.select_one(".a-price-whole") or soup.select_one(".apexPriceToPay .a-offscreen")
            
            if price_tag:
                price_raw = price_tag.get_text().replace(",", "").replace("₹", "").strip()
                price = int("".join(filter(str.isdigit, price_raw.split('.')[0])))
                return {"Timestamp": datetime.now(IST).strftime("%Y-%m-%d %H:%M"), "Product": title, "Price": price, "URL": url}
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

def run_price_tracker():
    run_time = datetime.now(IST).strftime("%Y-%m-%d %H:%M")

    if os.path.exists(FILENAME):
        df = pd.read_excel(FILENAME)
    else:
        df = pd.DataFrame(columns=["SKU Name"])

    if "SKU Name" not in df.columns:
        df.insert(0, "SKU Name", "")

    # Insert latest price column first
    df.insert(1, run_time, "")

    random.shuffle(URLS)

    for i, url in enumerate(URLS):
        print(f"[{i+1}/{len(URLS)}] Checking product...")
        data = get_amazon_data(url)
        if not data: continue

        sku = data["Product"]
        price = data["Price"]

        if sku in df["SKU Name"].values:
            df.loc[df["SKU Name"] == sku, run_time] = price
        else:
            new_row = {col: "" for col in df.columns}
            new_row["SKU Name"] = sku
            new_row[run_time] = price
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Format Excel for better readability
    with pd.ExcelWriter(FILENAME, engine='openpyxl', mode='w') as writer:
        df.to_excel(writer, index=False)
        worksheet = writer.sheets['Sheet1']
        for col_cells in worksheet.columns:
            length = max(len(str(cell.value)) for cell in col_cells)
            worksheet.column_dimensions[col_cells[0].column_letter].width = length + 5

    print("✅ Latest price inserted first. Older prices shifted right.")

if __name__ == "__main__":
    while True:
        run_price_tracker()
        print("⏰ Waiting 1 hour before next fetch...")
        time.sleep(3600)  # 1 hour
