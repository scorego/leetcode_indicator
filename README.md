# LeetCode Indicator

A small static site that visualizes LeetCode problem online user counts over time.

## Features
- Main trend chart (Chart.js) and a compact overview chart for drag-to-select ranges.
- Supports hourly and daily (daily = per-day maximum) aggregation.
- Localized UI: English and Chinese (legend shows Chinese problem names when `中文` selected).
- Displays LeetCode problem IDs and English names in tooltips.

## Quick start (serve locally)
1. Open a terminal in the project root (`d:\code\github\leetcode_indicator`).
2. Run a lightweight HTTP server (so `fetch` can load the JSON):

```powershell
python -m http.server 8000
```

3. Open your browser to: http://localhost:8000

## Data
- The site reads `data/online_users.json` (array of timestamped records).
- Each record structure:
```json
{
	"timestamp": "2026-01-28T06:00:00",
	"site": "us",
	"problems": [
		{ "name": "Two Sum", "online_users": 1900 },
		...
	]
}
```

## Customizing problems metadata
- The file `index.html` contains a `problemsMeta` mapping used to show LeetCode ids and Chinese names.
- To add or change entries, edit the `problemsMeta` object near the top of the script, e.g.:
```js
'Two Sum': { id: 1, zh: '两数之和' }
```

## Notes / Troubleshooting
- Always serve the files over HTTP; opening `index.html` directly via `file://` will block `fetch` requests to local JSON files.
- If the chart doesn't render, open DevTools → Console and Network to check for errors or failed requests.

## License
- MIT-style (you can adapt as needed).

If you want, I can:
- Move `problemsMeta` into a JSON file and fetch it dynamically.
- Add a small info panel showing the mapping and links to each LeetCode problem.
- Add automated build/test steps.
