```python
import requests
from bs4 import BeautifulSoup
import datetime
import re
from googlesearch import search
import json
import time
import random
import tweepy  # Requires installation and API keys for Twitter/X scraping

# Pudding-Alpha0 Updated: Added social media scraping (VK, OK, Telegram, Twitter/X) and more comprehensive scraping (deeper content extraction, link following, increased results)

OUTPUT_FILE = "putin_osint.txt"

# Enhanced queries
QUERIES = [
    "Vladimir Putin current location",
    "Vladimir Putin latest news",
    "Vladimir Putin whereabouts today",
    "Vladimir Putin social media",
    "Путин текущее местоположение",
    "Путин последние новости",
    "Путин где сейчас",
    "Путин социальные сети"
]

# Expanded Russian-focused sources including social media
RUSSIAN_DOMAINS = [
    "site:kremlin.ru",
    "site:tass.ru",
    "site:ria.ru",
    "site:interfax.ru",
    "site:rt.com",
    "site:sputniknews.com",
    "site:vk.com",
    "site:ok.ru",
    "site:t.me",  # Telegram channels
    "site:mil.ru",
    "site:svr.gov.ru"
]

# General sources including global social media
GENERAL_DOMAINS = [
    "site:bbc.com",
    "site:cnn.com",
    "site:nytimes.com",
    "site:reuters.com",
    "site:apnews.com",
    "site:twitter.com",  # Now X
    "site:facebook.com",
    "site:instagram.com"
]

# Twitter API setup (user must provide keys)
TWITTER_API_KEY = "YOUR_API_KEY"
TWITTER_API_SECRET = "YOUR_API_SECRET"
TWITTER_ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
TWITTER_ACCESS_SECRET = "YOUR_ACCESS_SECRET"

def setup_twitter_api():
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
    return tweepy.API(auth)

def scrape_twitter(query, api, count=20):
    try:
        tweets = api.search_tweets(q=query, count=count, lang="ru,en", tweet_mode="extended")
        return [tweet.full_text for tweet in tweets]
    except Exception as e:
        print(f"Twitter scrape error: {e}")
        return []

def fetch_search_results(query, num_results=20, lang='en'):  # Increased results
    results = []
    try:
        for url in search(query, num_results=num_results, lang=lang, advanced=True):
            results.append({
                'title': url.title,
                'url': url.url,
                'description': url.description
            })
        time.sleep(random.uniform(1, 3))
    except Exception as e:
        print(f"Error searching {query}: {e}")
    return results

def scrape_page(url, depth=1):  # Added depth for more comprehensive scraping
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = ' '.join([p.text for p in soup.find_all('p')])
        content = re.sub(r'\s+', ' ', text)[:5000]  # Increased truncate limit

        if depth > 0:
            links = [a['href'] for a in soup.find_all('a', href=True) if 'putin' in a['href'].lower()][:5]  # Follow up to 5 relevant links
            for link in links:
                if link.startswith('/'):
                    link = url + link
                elif not link.startswith('http'):
                    continue
                sub_content = scrape_page(link, depth-1)
                content += ' ' + sub_content

        return content
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return ""

def gather_intel():
    intel = {
        'timestamp': datetime.datetime.now().isoformat(),
        'sources': [],
        'whereabouts': [],
        'news': [],
        'social_media': []
    }

    twitter_api = setup_twitter_api()

    # Search English sources
    for query in QUERIES[:4]:
        for domain in GENERAL_DOMAINS:
            full_query = f"{query} {domain}"
            results = fetch_search_results(full_query, num_results=10)
            for res in results:
                content = scrape_page(res['url'], depth=2)  # Deeper scrape
                intel['sources'].append({
                    'query': full_query,
                    'url': res['url'],
                    'title': res['title'],
                    'content': content
                })
                if 'location' in content.lower() or 'where' in content.lower():
                    intel['whereabouts'].append(content)
                if 'social' in query.lower():
                    intel['social_media'].append(content)

    # Search Russian sources
    for query in QUERIES[4:]:
        for domain in RUSSIAN_DOMAINS:
            full_query = f"{query} {domain}"
            results = fetch_search_results(full_query, num_results=10, lang='ru')
            for res in results:
                content = scrape_page(res['url'], depth=2)
                intel['sources'].append({
                    'query': full_query,
                    'url': res['url'],
                    'title': res['title'],
                    'content': content
                })
                if 'местоположение' in content.lower() or 'где' in content.lower():
                    intel['whereabouts'].append(content)
                if 'социальные' in query.lower():
                    intel['social_media'].append(content)

    # Specific social media scraping
    twitter_content = scrape_twitter("Vladimir Putin", twitter_api)
    intel['social_media'].extend(twitter_content)

    # Broad search
    broad_results = fetch_search_results("Vladimir Putin OSINT", num_results=30)
    for res in broad_results:
        content = scrape_page(res['url'], depth=1)
        intel['news'].append(content)

    return intel

def save_to_file(intel):
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(json.dumps(intel, ensure_ascii=False, indent=4))
    print(f"Intelligence saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    intel = gather_intel()
    save_to_file(intel)
```
