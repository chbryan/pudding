# pudding
OSINT tool for gathering intelligence on Vladimir Putin, focusing on current whereabouts from global and Russian sources.

## Features
- Searches web, news, and social media (X/Twitter, VK, OK, Telegram).
- Scrapes content deeply, follows links.
- Prioritizes Russian sites: kremlin.ru, tass.ru, etc.
- Outputs to `putin_osint.txt` in JSON.

## Requirements
- Python 3.x
- Libraries: `requests`, `beautifulsoup4`, `googlesearch-python`, `tweepy`
- Twitter API keys (set in script).

## Installation
```
pip install requests beautifulsoup4 googlesearch-python tweepy
```

## Usage
1. Set Twitter API keys in script.
2. Run: `python pudding-alpha0.py`

## Output
JSON file with timestamp, sources, whereabouts, news, social media.

## Notes
- Respects rate limits with delays.
- For CIA-like use; handle ethically.
