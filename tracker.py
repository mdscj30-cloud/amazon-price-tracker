import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import random
import os

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

FILENAME = "price_tracker_final.xlsx"

def get_data(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    try:
        time.sleep(random.uniform(2, 5))
        res = requests.get(url, headers=headers, timeout=20)
        soup = BeautifulSoup(res.content, "html.parser")
        title = soup.find(id="productTitle").get_text().strip()
        price_raw = soup.select_one(".a-price-whole").get_text().replace(",", "")
        price = int("".join(filter(str.isdigit, price_raw.split('.')[0])))
        return {"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"), "Product": title, "Price": price, "URL": url}
    except: return None

# Load old data
df_old = pd.read_excel(FILENAME) if os.path.exists(FILENAME) else pd.DataFrame()

# Scrape new data
new_results = []
for url in URLS:
    data = get_data(url)
    if data: new_results.append(data)

# Combine and Save
df_new = pd.DataFrame(new_results)
df_final = pd.concat([df_old, df_new], ignore_index=True)
df_final.to_excel(FILENAME, index=False)
