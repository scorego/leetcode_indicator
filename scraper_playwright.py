from playwright.sync_api import sync_playwright
import re
import json
import os
from datetime import datetime, timedelta

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "online_users.json")

PROBLEMS = [
    {"name": "Two Sum", "slug": "two-sum"},
    {"name": "Add Two Numbers", "slug": "add-two-numbers"},
    {"name": "Longest Substring Without Repeating Characters", "slug": "longest-substring-without-repeating-characters"},
    {"name": "Median of Two Sorted Arrays", "slug": "median-of-two-sorted-arrays"},
    {"name": "Longest Palindromic Substring", "slug": "longest-palindromic-substring"},
]

LEETCODE_SITES = {
    "us": "https://leetcode.com",
    "cn": "https://leetcode.cn",
}

def save_data(data):
    existing_data = []
    THIRTY_DAYS_AGO = datetime.now() - timedelta(days=30)

    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except json.JSONDecodeError:
            existing_data = []

    existing_data.append(data)

    filtered = []
    filtered_out = []

    for item in existing_data:
        try:
            ts = datetime.fromisoformat(item['timestamp'])
        except (KeyError, ValueError):
            continue

        if ts >= THIRTY_DAYS_AGO:
            filtered.append(item)
        else:
            filtered_out.append(item)

    # Safe atomic write
    tmp_file = DATA_FILE + ".tmp"
    with open(tmp_file, 'w', encoding='utf-8') as f:
        json.dump(filtered, f, indent=2, ensure_ascii=False)

    os.replace(tmp_file, DATA_FILE)

    if filtered_out:
        archive_date = THIRTY_DAYS_AGO.strftime("%Y-%m-%d")
        archive_dir = os.path.join(DATA_DIR, archive_date)
        os.makedirs(archive_dir, exist_ok=True)

        pre_data_file = os.path.join(archive_dir, "online_users.json")

        with open(pre_data_file, 'w', encoding='utf-8') as f:
            json.dump(filtered_out, f, indent=2, ensure_ascii=False)


def extract_online_from_text(text):
    # try patterns like '1,234 online', '1234 users online', '在线 1234' etc.
    patterns = [r"(\d{1,3}(?:,\d{3})*)\s*(?:online|users)", r"在线[:\s]*(\d{1,3}(?:,\d{3})*)", r"(\d{1,3}(?:,\d{3})*)\s*人"]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return int(m.group(1).replace(',', ''))
    return 0


def extract_online_from_page(page):
    # Try to locate visible text nodes matching common patterns using Playwright locators (more reliable)
    patterns = [r"\d{1,3}(?:,\d{3})*\s*(?:online|users)", r"在线[:\s]*\d{1,3}(?:,\d{3})*", r"\d{1,3}(?:,\d{3})*\s*人"]
    for pat in patterns:
        try:
            locator = page.locator(f"text=/{pat}/i").first()
            if locator and locator.count() and locator.count() > 0:
                txt = locator.inner_text()
                m = re.search(r"(\d{1,3}(?:,\d{3})*)", txt)
                if m:
                    return int(m.group(1).replace(',', ''))
        except Exception:
            continue
    return None


def run(site='us'):
    base = LEETCODE_SITES.get(site)
    if not base:
        print('Unknown site', site)
        return
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36')
        page = context.new_page()
        # increase navigation and action timeouts (120s)
        page.set_default_navigation_timeout(120000)
        page.set_default_timeout(120000)

        for prob in PROBLEMS:
            max_retries = 2
            while max_retries > 0:
                url = f"{base}/problems/{prob['slug']}/"
                try:
                    page.goto(url, wait_until='networkidle', timeout=120000)
                    text = page.content()
                    count = extract_online_from_text(text)
                    print(f"{prob['name']}: {count}")
                    if count > 0:
                        results.append({"name": prob['name'], "online_users": count})
                        max_retries = 0  # success, exit retry loop
                except Exception as e:
                    print('Error', url, e)
                    max_retries -= 1
        browser.close()
    data = {"timestamp": datetime.now().isoformat(), "site": site, "problems": results}
    save_data(data)
    print('Saved')


if __name__ == '__main__':
    import sys
    site = sys.argv[1] if len(sys.argv) > 1 else 'us'
    run(site)
