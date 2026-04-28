"""
smart-web-scraper
-----------------
A clean, modular Python web scraping toolkit.

Modules:
    scraper  – HTTP fetching with retries and User-Agent rotation
    parser   – HTML parsing and data extraction
    storage  – CSV and JSON output
"""

from .scraper import fetch_page, build_session
from .parser  import parse_quotes, get_next_page
from .storage import save_csv, save_json

__all__ = [
    "fetch_page",
    "build_session",
    "parse_quotes",
    "get_next_page",
    "save_csv",
    "save_json",
]
