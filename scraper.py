import asyncio
import aiohttp
import csv
import json
import random
import time
import yaml
from bs4 import BeautifulSoup
from typing import Dict, List, Optional


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/118.0.0.0 Safari/537.36",
]


class WebScraper:
    def __init__(self, config: str = None):
        self.config = self._load_config(config) if config else {}
        self.session = None
        self.results = []

    def _load_config(self, path: str) -> dict:
        with open(path, "r") as f:
            return yaml.safe_load(f)

    def _get_headers(self) -> dict:
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }

    async def _fetch(self, url: str) -> str:
        settings = self.config.get("settings", {})
        delay = settings.get("delay", [1, 2])
        timeout = settings.get("timeout", 30)

        await asyncio.sleep(random.uniform(*delay))

        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, headers=self._get_headers(), timeout=aiohttp.ClientTimeout(total=timeout)
            ) as resp:
                return await resp.text()

    def _parse(self, html: str, selectors: Dict[str, str]) -> Dict[str, str]:
        soup = BeautifulSoup(html, "html.parser")
        result = {}
        for key, selector in selectors.items():
            element = soup.select_one(selector)
            result[key] = element.get_text(strip=True) if element else None
        return result

    def run(self, url: str, selectors: Dict[str, str]) -> List[Dict]:
        html = asyncio.run(self._fetch(url))
        data = self._parse(html, selectors)
        self.results.append(data)
        return self.results

    def run_multiple(self, urls: List[str], selectors: Dict[str, str]) -> List[Dict]:
        for url in urls:
            self.run(url, selectors)
        return self.results

    def export(self, data: List[Dict], format: str = "csv", filename: str = "output"):
        if format == "csv":
            self._export_csv(data, filename)
        elif format == "json":
            self._export_json(data, filename)

    def _export_csv(self, data: List[Dict], filename: str):
        if not data:
            return
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)

    def _export_json(self, data: List[Dict], filename: str):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Web Scraper Toolkit")
    parser.add_argument("--config", type=str, help="Config YAML file")
    parser.add_argument("--url", type=str, required=True)
    parser.add_argument("--output", type=str, default="results.csv")
    args = parser.parse_args()

    scraper = WebScraper(config=args.config)
    selectors = scraper.config.get("selectors", {})
    data = scraper.run(url=args.url, selectors=selectors)
    scraper.export(data, format="csv", filename=args.output)
    print(f"Scraped {len(data)} items -> {args.output}")
