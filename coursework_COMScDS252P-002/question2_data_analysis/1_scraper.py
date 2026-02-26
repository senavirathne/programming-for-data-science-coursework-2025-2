"""Scrape book data and save to data/raw_books_data.csv."""

from __future__ import annotations

import csv
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
BOOKS_TARGET = 100
REQUEST_DELAY_SECONDS = 1.0

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
OUTPUT_FILE = DATA_DIR / "raw_books_data.csv"


def get_soup(url: str, retries: int = 3) -> BeautifulSoup | None:
    """Fetch URL with retries and return parsed soup."""
    for attempt in range(1, retries + 1):
        try:
            print(f"Fetching URL (attempt {attempt}/{retries}): {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except requests.exceptions.RequestException:
            time.sleep(2)
    return None


def scrape_book_details(book_url: str) -> dict[str, str] | None:
    """Scrape title, price, rating, category, and availability for one book."""
    soup = get_soup(book_url)
    if soup is None:
        return None

    product_main = soup.find("div", class_="product_main")
    if product_main is None:
        return None

    title_tag = product_main.find("h1")
    price_tag = product_main.find("p", class_="price_color")
    rating_tag = product_main.find("p", class_="star-rating")
    availability_tag = product_main.find("p", class_="instock availability")
    breadcrumb = soup.find("ul", class_="breadcrumb")

    title = title_tag.text.strip() if title_tag else "Unknown"
    price = price_tag.text.strip() if price_tag else "Unknown"
    rating = rating_tag["class"][1] if rating_tag and len(rating_tag.get("class", [])) > 1 else "Unknown"
    availability = availability_tag.text.strip() if availability_tag else "Unknown"
    category = "Unknown"
    if breadcrumb:
        crumbs = breadcrumb.find_all("li")
        if len(crumbs) > 2:
            category = crumbs[2].text.strip()

    return {
        "Title": title,
        "Price": price,
        "Rating": rating,
        "Category": category,
        "Availability": availability,
    }


def scrape_catalogue(min_books: int = BOOKS_TARGET) -> list[dict[str, str]]:
    """Scrape at least min_books from books.toscrape.com."""
    books_data: list[dict[str, str]] = []
    page = 1

    while len(books_data) < min_books:
        url = BASE_URL.format(page)
        soup = get_soup(url)
        if soup is None:
            break

        articles = soup.find_all("article", class_="product_pod")
        if not articles:
            break

        for article in articles:
            if len(books_data) >= min_books:
                break

            link_tag = article.find("h3").find("a") if article.find("h3") else None
            if link_tag is None or "href" not in link_tag.attrs:
                continue

            book_url = urljoin(url, link_tag["href"])
            book_details = scrape_book_details(book_url)
            if book_details:
                books_data.append(book_details)

            time.sleep(REQUEST_DELAY_SECONDS)

        page += 1

    return books_data


def save_to_csv(data: list[dict[str, str]], filename: Path) -> None:
    """Save raw scraped records to CSV."""
    filename.parent.mkdir(parents=True, exist_ok=True)
    keys = ["Title", "Price", "Rating", "Category", "Availability"]
    with filename.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    records = scrape_catalogue(BOOKS_TARGET)
    save_to_csv(records, OUTPUT_FILE)
    print(f"Saved {len(records)} records to {OUTPUT_FILE}")
