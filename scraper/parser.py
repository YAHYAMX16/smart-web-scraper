"""
parser.py
---------
Parses raw HTML into structured Python dictionaries.
Uses BeautifulSoup for clean, readable extraction logic.
"""

import logging
from typing import Optional
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def parse_quotes(html: str) -> list[dict]:
    """
    Extract quotes from quotes.toscrape.com HTML.

    Each quote is returned as a dictionary with:
        - text  : the quote content
        - author: the author's name
        - tags  : list of topic tags

    Args:
        html: Raw HTML string from the page.

    Returns:
        List of quote dictionaries. Empty list if parsing fails.
    """
    if not html:
        logger.warning("Empty HTML passed to parser.")
        return []

    soup = BeautifulSoup(html, "html.parser")
    quotes = []

    for item in soup.select("div.quote"):
        try:
            text   = item.select_one("span.text").get_text(strip=True)
            author = item.select_one("small.author").get_text(strip=True)
            tags   = [tag.get_text(strip=True) for tag in item.select("a.tag")]

            # Remove surrounding quotation marks if present
            text = text.strip("\u201c\u201d")

            quotes.append({
                "text":   text,
                "author": author,
                "tags":   tags,
            })

        except AttributeError as e:
            logger.warning(f"Skipped malformed quote block: {e}")
            continue

    logger.info(f"Parsed {len(quotes)} quotes from page.")
    return quotes


def get_next_page(html: str) -> Optional[str]:
    """
    Find the relative URL of the next page, if it exists.

    Args:
        html: Raw HTML string.

    Returns:
        Relative URL string (e.g. '/page/2/') or None if no next page.
    """
    soup = BeautifulSoup(html, "html.parser")
    next_btn = soup.select_one("li.next > a")
    if next_btn:
        href = next_btn.get("href")
        logger.debug(f"Next page found: {href}")
        return href
    return None
