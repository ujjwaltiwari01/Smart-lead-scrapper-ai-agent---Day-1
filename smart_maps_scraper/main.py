import os
import re
import time
import random
import requests
import pandas as pd
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

load_dotenv()

STOP_FLAG = False

def stop_scraping():
    global STOP_FLAG
    STOP_FLAG = True

def reset_stop_flag():
    global STOP_FLAG
    STOP_FLAG = False


# ---------- Setup WebDriver ----------
def setup_driver():
    edge_options = Options()
    edge_options.use_chromium = True
    edge_options.add_argument("--headless")
    edge_options.add_argument("--disable-gpu")
    edge_options.add_argument("--disable-blink-features=AutomationControlled")
    edge_options.add_argument("--log-level=3")
    edge_options.add_argument("--window-size=1920,1080")
    service = Service("msedgedriver.exe")
    return webdriver.Edge(service=service, options=edge_options)


# ---------- Extract email & phone ----------
def extract_from_website(url):
    if not url or url == "N/A":
        return {"Email": "N/A", "Phone": "N/A"}

    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=(6, 12))
        if resp.status_code != 200:
            return {"Email": "N/A", "Phone": "N/A"}

        html = resp.text
        emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", html))
        emails = [e for e in emails if not any(b in e.lower() for b in ["example.com", "google.com", "wixpress.com"])]
        email = emails[0] if emails else "N/A"

        phones = re.findall(r"\+?\d[\d\s\-\(\)]{7,}\d", html)
        phone = "N/A"
        for p in phones:
            p = re.sub(r"[^\d+]", "", p)
            if len(p) >= 10:
                phone = p
                break

        return {"Email": email, "Phone": phone}

    except Exception:
        return {"Email": "N/A", "Phone": "N/A"}


# ---------- Google Fallback ----------
def find_website_fallback(name, city):
    try:
        q = f"{name} {city}"
        resp = requests.get("https://www.google.com/search?q=" + quote(q), headers={"User-Agent": "Mozilla/5.0"}, timeout=8)
        links = re.findall(r'<a href="/url\?q=(https://[^&]+)&', resp.text)
        for l in links:
            if not any(x in l for x in ["google.com", "facebook.com", "youtube.com"]):
                return l
    except:
        pass
    return None


# ---------- Google Maps Scraper ----------
def scrape_google_maps(city, business, progress_callback=None, max_items=500):
    """Scrape up to 500 listings."""
    reset_stop_flag()
    driver = setup_driver()
    query = f"https://www.google.com/maps/search/{quote(business)}+in+{quote(city)}"
    driver.get(query)

    if progress_callback:
        progress_callback(f"🔎 Searching '{business}' in {city}...")

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[role="feed"]'))
        )
    except:
        driver.quit()
        return []

    feed = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
    scroll_count = 0
    while scroll_count < 60 and not STOP_FLAG:  # Scroll more times for more results
        driver.execute_script("arguments[0].scrollTop += 2000;", feed)
        time.sleep(random.uniform(1.0, 1.4))
        scroll_count += 1

    listings = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/maps/place/"]')
    links = []
    for l in listings:
        href = l.get_attribute("href")
        if href and "/maps/place/" in href and href not in links:
            links.append(href)
    links = links[:max_items]

    results = []
    for i, link in enumerate(links):
        if STOP_FLAG:
            break
        try:
            driver.get(link)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'h1'))
            )
            try:
                name = driver.find_element(By.CSS_SELECTOR, 'h1.DUwDvf').text.strip()
            except:
                name = driver.find_element(By.CSS_SELECTOR, 'h1.fontHeadlineLarge').text.strip()

            try:
                website_elem = driver.find_element(By.CSS_SELECTOR, 'a[data-item-id="authority"]')
                website = website_elem.get_attribute("href")
            except:
                website = None

            if not website:
                website = find_website_fallback(name, city)

            results.append({
                "Name": name,
                "Website": website or "N/A"
            })
            if progress_callback:
                progress_callback(f"✅ {i+1}/{len(links)} — {name}")

        except Exception as e:
            print(f"Error ({i}): {e}")
            continue

    driver.quit()
    return results


# ---------- Main pipeline ----------
def generate_leads(city, business, progress_callback=None, max_items=500):
    data = scrape_google_maps(city, business, progress_callback, max_items=max_items)

    with ThreadPoolExecutor(max_workers=6) as executor:
        details = list(executor.map(lambda d: extract_from_website(d["Website"]), data))

    for i in range(len(data)):
        data[i].update(details[i])

    os.makedirs("output", exist_ok=True)
    out_path = f"output/final_leads_{int(time.time())}.csv"
    df = pd.DataFrame(data)[["Name", "Website", "Email", "Phone"]]
    df.to_csv(out_path, index=False)

    if progress_callback:
        progress_callback(f"💾 Saved: {out_path}")
    return out_path, len(data)
