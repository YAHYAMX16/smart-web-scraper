"""
scraper.py
----------
Core scraping engine.
Handles HTTP requests, retries, and raw HTML fetching.
"""

import time
import random
import logging
import requests
from typing import Optional
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


# ── User-Agent pool to rotate and avoid blocks ──────────────────────────────
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
]


def build_session(retries: int = 3, backoff: float = 0.5) -> requests.Session:
    """
    Create a requests.Session with automatic retry logic.

    Args:
        retries:  Number of retry attempts on failure.
        backoff:  Backoff factor between retries (seconds).

    Returns:
        A configured requests.Session object.
    """
    session = requests.Session()
    retry_strategy = Retry(
        total=retries,
        backoff_factor=backoff,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def fetch_page(
    url: str,
    session: Optional[requests.Session] = None,
    timeout: int = 10,
    delay: float = 1.0,
) -> Optional[str]:
    """
    Fetch raw HTML from a URL with a random User-Agent and polite delay.

    Args:
        url:     Target URL to scrape.
        session: Optional reusable session (creates one if not provided).
        timeout: Request timeout in seconds.
        delay:   Minimum delay between requests (adds random jitter).

    Returns:
        HTML content as a string, or None if the request failed.
    """
    if session is None:
        session = build_session()

    headers = {"User-Agent": random.choice(USER_AGENTS)}

    # Polite delay to avoid hammering the server
    time.sleep(delay + random.uniform(0.1, 0.5))

    try:
        response = session.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        logger.info(f"[OK] Fetched: {url} — status {response.status_code}")
        return response.text

    except requests.exceptions.HTTPError as e:
        logger.error(f"[HTTP Error] {url} — {e}")
    except requests.exceptions.ConnectionError:
        logger.error(f"[Connection Error] Could not reach: {url}")
    except requests.exceptions.Timeout:
        logger.error(f"[Timeout] Request timed out: {url}")
    except requests.exceptions.RequestException as e:
        logger.error(f"[Request Failed] {url} — {e}")

    return None
