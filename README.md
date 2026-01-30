# LeetCode Indicator

A small static site that visualizes LeetCode problem online user counts over time.

## Features
- Main trend chart (Chart.js) and a compact overview chart for drag-to-select ranges.
- Supports hourly and daily (daily = per-day maximum) aggregation.

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