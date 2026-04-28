# 🕷️ Smart Web Scraper

A clean, modular Python automation tool for scraping structured data from websites — built with reliability, readability, and real-world use in mind.

---

## ✨ Features

- **Multi-page scraping** — automatically follows pagination
- **Retry logic** — handles timeouts and server errors gracefully
- **User-Agent rotation** — reduces chance of being blocked
- **Polite delays** — respects servers with randomized wait times
- **Dual output** — saves results as both **CSV** and **JSON**
- **CLI interface** — fully configurable from the command line
- **Modular design** — clean separation of fetch / parse / store logic

---

## 📁 Project Structure

```
smart-web-scraper/
├── main.py               # Entry point & CLI runner
├── requirements.txt      # Dependencies
├── .gitignore
├── scraper/
│   ├── __init__.py       # Public API
│   ├── scraper.py        # HTTP fetching + session management
│   ├── parser.py         # HTML parsing with BeautifulSoup
│   └── storage.py        # CSV & JSON output
└── data/                 # Output files (auto-generated, not tracked)
```

---

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/smart-web-scraper.git
cd smart-web-scraper
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the scraper
```bash
# Default: scrape up to 10 pages
python main.py

# Custom: 5 pages, 2s delay, custom output name
python main.py --pages 5 --delay 2.0 --output my_data
```

---

## ⚙️ CLI Options

| Flag | Default | Description |
|------|---------|-------------|
| `--pages` | `10` | Maximum number of pages to scrape |
| `--delay` | `1.0` | Seconds to wait between requests |
| `--output` | `quotes` | Base name for output files |

---

## 📄 Output Example

**CSV** (`data/quotes_20241201_143022.csv`):
```
text,author,tags
The world as we have created it...,Albert Einstein,change | deep-thoughts | ...
It is our choices...,J.K. Rowling,choices | ...
```

**JSON** (`data/quotes_20241201_143022.json`):
```json
[
  {
    "text": "The world as we have created it...",
    "author": "Albert Einstein",
    "tags": ["change", "deep-thoughts", "thinking"]
  }
]
```

---

## 🧠 How It Works

```
main.py
  │
  ├── scraper.py   →  fetch_page()      # GET request + retry + User-Agent
  ├── parser.py    →  parse_quotes()    # BeautifulSoup extraction
  │                   get_next_page()   # Pagination detection
  └── storage.py   →  save_csv()        # Timestamped CSV output
                      save_json()       # Timestamped JSON output
```

---

## 🔧 Extending the Scraper

To scrape a different website, only `parser.py` needs to change:

```python
# parser.py — replace parse_quotes() with your own logic
def parse_products(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    products = []
    for item in soup.select("div.product-card"):
        products.append({
            "name":  item.select_one("h2.title").get_text(strip=True),
            "price": item.select_one("span.price").get_text(strip=True),
        })
    return products
```

The fetch and storage logic stays the same — that's the power of modular design.

---

## 📋 Requirements

- Python 3.10+
- requests
- beautifulsoup4

---

## 👤 Author

**Yahya Modaria** — Python Developer & Data Automation Specialist  
📍 Marrakech, Morocco  
📧 yahyamodaria33@gmail.com

---

## 📜 License

MIT License — free to use, modify, and distribute.
