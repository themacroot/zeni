import hashlib
import os
import time
import re
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# Config
BASE_URL = "https://website.rbi.org.in/web/rbi/notifications/master-directions?delta=200"
ROOT_URL = "https://website.rbi.org.in"
DOWNLOAD_DIR = "../resource/rbi/directions/rbi_master_directions"

# Create download directory if it doesn't exist
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Set up headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless=new")
driver = webdriver.Chrome(options=chrome_options)

# Load the initial page
driver.get(BASE_URL)
time.sleep(3)

pdf_entries = []


def sanitize_filename(name, max_length=150):
    # Replace illegal characters
    safe_name = re.sub(r'[\\/*?:"<>|]', "_", name).strip()

    # If name is too long, truncate and append a hash
    if len(safe_name) > max_length:
        hash_suffix = hashlib.md5(safe_name.encode()).hexdigest()[:6]
        safe_name = safe_name[:max_length - 7] + "_" + hash_suffix  # 7 = 1 (_) + 6 (hash)

    return safe_name

def extract_links_with_titles():
    soup = BeautifulSoup(driver.page_source, "html.parser")
    rows = soup.select(".notification-row-each-inner")
    for row in rows:
        heading_tag = row.select_one(".mtm_list_item_heading.truncatedContent.font-resized")
        download_link_tag = row.select_one("a.matomo_download.download_link")

        if heading_tag and download_link_tag:
            title = sanitize_filename(heading_tag.get_text(strip=True))
            href = download_link_tag["href"]
            full_url = urljoin(ROOT_URL, href)
            pdf_entries.append((full_url, title))

# Scrape the first page
extract_links_with_titles()

# Paginate through all available pages
while True:
    try:
        next_btn = driver.find_element(By.CSS_SELECTOR, "a[aria-label='Next']")
        if 'disabled' in next_btn.get_attribute("class"):
            break
        next_btn.click()
        time.sleep(2)
        extract_links_with_titles()
    except Exception as e:
        print("No more pages or pagination failed:", e)
        break

print(f"Found {len(pdf_entries)} PDF files to download.")

# Download each PDF with a meaningful filename
for url, title in pdf_entries:
    filename = os.path.join(DOWNLOAD_DIR, f"{title}.pdf")

    print(f"📥 Downloading: {url} → {filename}")
    try:
        r = requests.get(url)
        r.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(r.content)
    except Exception as e:
        print(f"❌ Failed to download {url}: {e}")

# Cleanup
driver.quit()
print("✅ All downloads complete.")
