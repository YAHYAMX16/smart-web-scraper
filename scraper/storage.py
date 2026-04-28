"""
storage.py
----------
Handles saving scraped data to CSV and JSON formats.
Provides clean output with timestamps for traceability.
"""

import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

OUTPUT_DIR = Path(__file__).parent.parent / "data"
OUTPUT_DIR.mkdir(exist_ok=True)


def _timestamped_filename(base: str, ext: str) -> Path:
    """Generate a filename with a timestamp to avoid overwriting old results."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return OUTPUT_DIR / f"{base}_{timestamp}.{ext}"


def save_csv(data: list[dict], filename: str = "results") -> Path:
    """
    Save a list of dictionaries to a CSV file.

    Args:
        data:     List of dicts (all must share the same keys).
        filename: Base filename without extension.

    Returns:
        Path to the saved CSV file.

    Raises:
        ValueError: If data is empty.
    """
    if not data:
        raise ValueError("No data to save — list is empty.")

    filepath = _timestamped_filename(filename, "csv")
    fieldnames = list(data[0].keys())

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            # Flatten list fields (e.g. tags) to a pipe-separated string
            flat_row = {
                k: " | ".join(v) if isinstance(v, list) else v
                for k, v in row.items()
            }
            writer.writerow(flat_row)

    logger.info(f"Saved {len(data)} rows to CSV: {filepath}")
    return filepath


def save_json(data: Any, filename: str = "results") -> Path:
    """
    Save data to a pretty-printed JSON file.

    Args:
        data:     Any JSON-serializable object.
        filename: Base filename without extension.

    Returns:
        Path to the saved JSON file.
    """
    filepath = _timestamped_filename(filename, "json")

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    logger.info(f"Saved JSON to: {filepath}")
    return filepath
