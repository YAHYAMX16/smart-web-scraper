"""
main.py
-------
Entry point for the Smart Web Scraper.
Runs a full multi-page scrape and saves results to CSV and JSON.

Usage:
    python main.py
    python main.py --pages 5
    python main.py --pages 3 --delay 2.0 --output my_results
"""

import argparse
import logging
import sys
from scraper import (
    build_session,
    fetch_page,
    parse_quotes,
    get_next_page,
    save_csv,
    save_json,
)

# ── Logging setup ────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

BASE_URL = "https://quotes.toscrape.com"


def run(max_pages: int = 10, delay: float = 1.0, output: str = "quotes") -> list[dict]:
    """
    Scrape quotes from quotes.toscrape.com across multiple pages.

    Args:
        max_pages: Maximum number of pages to scrape.
        delay:     Delay in seconds between requests (polite scraping).
        output:    Base name for output files.

    Returns:
        List of all scraped quote dictionaries.
    """
    session   = build_session()
    all_data  = []
    next_path = "/"
    page_num  = 1

    logger.info(f"Starting scrape — max pages: {max_pages}, delay: {delay}s")

    while next_path and page_num <= max_pages:
        url  = BASE_URL + next_path
        logger.info(f"Scraping page {page_num}: {url}")

        html = fetch_page(url, session=session, delay=delay)
        if not html:
            logger.error(f"Failed to fetch page {page_num}. Stopping.")
            break

        quotes    = parse_quotes(html)
        all_data.extend(quotes)
        next_path = get_next_page(html)
        page_num += 1

    if not all_data:
        logger.warning("No data collected. Exiting.")
        return []

    # ── Save results ─────────────────────────────────────────────────────────
    csv_path  = save_csv(all_data,  filename=output)
    json_path = save_json(all_data, filename=output)

    logger.info(f"Done! Scraped {len(all_data)} quotes from {page_num - 1} pages.")
    logger.info(f"  CSV  → {csv_path}")
    logger.info(f"  JSON → {json_path}")

    return all_data


def main():
    parser = argparse.ArgumentParser(
        description="Smart Web Scraper — Python Automation Tool by Yahya Modaria"
    )
    parser.add_argument(
        "--pages", type=int, default=10,
        help="Maximum number of pages to scrape (default: 10)"
    )
    parser.add_argument(
        "--delay", type=float, default=1.0,
        help="Delay between requests in seconds (default: 1.0)"
    )
    parser.add_argument(
        "--output", type=str, default="quotes",
        help="Base name for output files (default: quotes)"
    )

    args = parser.parse_args()
    results = run(max_pages=args.pages, delay=args.delay, output=args.output)

    if not results:
        sys.exit(1)

    # Print a quick preview
    print(f"\n{'─'*55}")
    print(f"  Preview — first 3 results:")
    print(f"{'─'*55}")
    for i, q in enumerate(results[:3], 1):
        print(f"\n  [{i}] \"{q['text'][:70]}...\"")
        print(f"       — {q['author']}")
        print(f"       Tags: {', '.join(q['tags'])}")
    print(f"\n{'─'*55}")
    print(f"  Total: {len(results)} quotes collected.")
    print(f"{'─'*55}\n")


if __name__ == "__main__":
    main()
