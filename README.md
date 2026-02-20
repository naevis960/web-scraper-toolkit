# 🕷️ Web Scraper Toolkit

A powerful, flexible web scraping toolkit built with Python.

## Features
- 🔄 Multi-site support with configurable selectors
- 🛡️ Anti-detection (rotating user agents, delays, proxy support)
- 📦 Export to CSV, JSON, Excel
- ⚡ Async scraping for high performance
- 🔧 Easy configuration via YAML

## Quick Start

```bash
pip install -r requirements.txt
python scraper.py --config config.yaml --output results.csv
```

## Usage

```python
from scraper import WebScraper

scraper = WebScraper(config="config.yaml")
data = scraper.run(url="https://example.com", selectors={
    "title": "h1",
    "price": ".price",
    "description": ".desc"
})
scraper.export(data, format="csv", filename="results.csv")
```

## Configuration

```yaml
settings:
  delay: [1, 3]
  timeout: 30
  retries: 3
  proxy: null
  user_agent_rotation: true

selectors:
  title: "h1.product-title"
  price: "span.price"
  description: "div.description"
```

## License
MIT
