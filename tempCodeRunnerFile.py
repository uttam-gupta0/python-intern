"""
News Headline Scraper
---------------------
A simple, robust web scraper to collect top headlines from a news website and save them to a .txt file.

What's included:
- A single Python script (this file) that fetches an URL, extracts headline-like text from <h1>, <h2>, <h3> and common headline-like classes, deduplicates and saves results.
- CLI options: change URL, output file, max headlines, minimum headline length, and optional delay.

Requirements:
    pip install requests beautifulsoup4

Usage examples:
    python news_headline_scraper.py
    python news_headline_scraper.py --url "https://timesofindia.indiatimes.com" --max 30 --output toi_headlines.txt

Notes:
- This script uses heuristics (h1/h2/h3 & class name matching) so it will work reasonably across many news sites without site-specific selectors.
- Always respect a site's robots.txt and terms of service.

"""

import argparse
import requests
from bs4 import BeautifulSoup
import time
import sys
import os
import logging
import re
from collections import OrderedDict

# --------- Configuration / Defaults ---------
DEFAULT_URL = "https://www.bbc.com/news"
DEFAULT_OUTPUT = "headlines.txt"
DEFAULT_MAX = 20
DEFAULT_MIN_LEN = 15
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

# --------- Functions ---------

def fetch_html(url, headers=None, timeout=10):
    """Fetch HTML from a URL and return text. Raises requests.HTTPError on bad status."""
    headers = headers or HEADERS
    logging.debug(f"Fetching URL: {url}")
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def parse_headlines_from_soup(soup, min_len=DEFAULT_MIN_LEN, max_count=DEFAULT_MAX):
    """Extract headline-like text from a BeautifulSoup object.

    Strategy:
      1. Collect text from <h1>, <h2>, <h3> tags.
      2. Also look for tags with class or id names containing headline/title keywords.
      3. Deduplicate while preserving order.
      4. Filter by length and return up to max_count items.
    """
    candidates = []

    # 1) h1/h2/h3
    for tag in soup.find_all(["h1", "h2", "h3"]):
        text = tag.get_text(separator=" ", strip=True)
        if text:
            candidates.append(text)

    # 2) classes/ids that look like headlines
    re_head = re.compile(r"headline|head|title|story|heading|lead", re.I)
    for tag in soup.find_all(True):  # all tags
        # check class names
        classes = tag.get("class") or []
        id_ = tag.get("id") or ""
        class_match = any(re_head.search(c) for c in classes) if classes else False
        id_match = bool(re_head.search(id_)) if id_ else False
        if class_match or id_match:
            text = tag.get_text(separator=" ", strip=True)
            if text:
                candidates.append(text)

    # 3) also collect anchor text that looks like headlines (e.g., big links)
    for a in soup.find_all("a"):
        text = a.get_text(separator=" ", strip=True)
        if text and len(text) >= min_len:
            # skip purely navigational short links
            candidates.append(text)

    # 4) filter, dedupe & preserve order
    dedup = OrderedDict()
    for t in candidates:
        norm = " ".join(t.split())  # normalize whitespace
        if len(norm) < min_len:
            continue
        # very short or punctuation-only skip
        if all(ch in "-–—:,.()[]{}'\"" for ch in norm):
            continue
        if norm not in dedup:
            dedup[norm] = True
        if len(dedup) >= max_count:
            break

    results = list(dedup.keys())
    logging.debug(f"Parsed {len(results)} candidate headlines")
    return results


def save_headlines(headlines, output_path):
    """Save headlines (list of strings) to output_path (one per line)."""
    with open(output_path, "w", encoding="utf-8") as f:
        for h in headlines:
            f.write(h + "\n")
    logging.info(f"Saved {len(headlines)} headlines to {output_path}")


# --------- CLI / Main ---------

def main():
    parser = argparse.ArgumentParser(description="Scrape top headlines from a news website and save to a text file.")
    parser.add_argument("--url", "-u", default=DEFAULT_URL, help="Target URL to scrape (default: BBC News homepage)")
    parser.add_argument("--output", "-o", default=DEFAULT_OUTPUT, help="Output .txt filename")
    parser.add_argument("--max", "-m", type=int, default=DEFAULT_MAX, help="Maximum number of headlines to save")
    parser.add_argument("--min-len", "-l", type=int, default=DEFAULT_MIN_LEN, help="Minimum length of headline to keep")
    parser.add_argument("--delay", "-d", type=float, default=0.0, help="Optional delay (seconds) before scraping")
    parser.add_argument("--show", action="store_true", help="Print headlines to console")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
    else:
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    if args.delay > 0:
        logging.info(f"Sleeping for {args.delay} seconds before request...")
        time.sleep(args.delay)

    try:
        html = fetch_html(args.url)
    except requests.RequestException as e:
        logging.error(f"Failed to fetch {args.url}: {e}")
        sys.exit(1)

    soup = BeautifulSoup(html, "html.parser")
    headlines = parse_headlines_from_soup(soup, min_len=args.min_len, max_count=args.max)

    if not headlines:
        logging.warning("No headlines found with current heuristics. Try increasing max or decreasing min-len, or provide a site-specific selector.")

    save_headlines(headlines, args.output)

    if args.show:
        print("\n=== Headlines ===")
        for i, h in enumerate(headlines, 1):
            print(f"{i}. {h}")

    logging.info("Done.")


if __name__ == "__main__":
    main()
