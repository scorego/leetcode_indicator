# LeetCode Indicator

A small static site that visualizes LeetCode problem online user counts over time.

See in https://scorego.github.io/leetcode_indicator/

## Features
- Main trend chart (Chart.js) and a compact overview chart for drag-to-select ranges.
- Supports hourly and daily (daily = per-day maximum) aggregation.

## Caching

The static page appends a cache-busting query parameter when loading JSON data files and requests them with `cache: no-store`, so users should see the latest collected data without needing a hard refresh.

GitHub Pages may still cache the HTML shell itself for a short period. If you change `index.html`, some users may briefly see the previous UI until that cache expires.

## Scraper (Playwright)

This project now uses a Playwright-based scraper that renders problem pages and extracts online-user counts.

Local run (recommended in a virtualenv):

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
source .venv/bin/activate # macOS / Linux
pip install -r requirements.txt
python -m playwright install --with-deps
# Run scraper for US and China
python scraper_playwright.py us
python scraper_playwright.py cn
```

CI: The GitHub Actions workflow has been updated to install Playwright and run `scraper_playwright.py` on schedule.

Notes:
- Playwright downloads browser binaries when `python -m playwright install` runs.
- The scraper is more resilient to anti-bot measures than a simple requests-based approach, but still may time out on some pages.
