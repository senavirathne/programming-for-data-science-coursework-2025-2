import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from urllib.parse import urljoin

# Configuration
BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
# We start at page 1.
OUTPUT_FILE = "books_raw.csv"
MIN_BOOKS = 100
PAGES_TO_SCRAPE = 50 # Set high enough, we break when we have enough books.


def get_soup(url, retries=3):
    """Fetches a URL and returns a BeautifulSoup object with manual retry logic."""
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            time.sleep(2)
    return None

def scrape_book_details(book_url):
    """Scrapes details from a specific book page."""
    soup = get_soup(book_url)
    if not soup:
        return None

    try:
        product_main = soup.find("div", class_="product_main")
        if not product_main:
            return None
            
        title = product_main.h1.text.strip()
        price = product_main.find("p", class_="price_color").text.strip()
        
        # Rating
        rating_tag = product_main.find("p", class_="star-rating")
        rating = rating_tag['class'][1] if rating_tag else "Unknown"
        
        # Availability
        availability_tag = product_main.find("p", class_="instock availability")
        availability = availability_tag.text.strip() if availability_tag else "Unknown"
        
        # Category
        breadcrumb = soup.find("ul", class_="breadcrumb")
        category = breadcrumb.find_all("li")[2].text.strip() if breadcrumb else "Unknown"
        
        return {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Category": category,
            "Availability": availability
        }
    except AttributeError as e:
        print(f"Error parsing details for {book_url}: {e}")
        return None

def scrape_catalogue(min_books=100):
    books_data = []
    page = 1
    
    print("Starting scraper...")
    
    while len(books_data) < min_books:
        url = BASE_URL.format(page)
        print(f"Scraping page {page}: {url}")
        
        soup = get_soup(url)
        if not soup:
            print(f"Failed to retrieve page {page}. Stopping.")
            break
        
        # Find all book links
        articles = soup.find_all("article", class_="product_pod")
        
        if not articles:
            print("No more books found.")
            break
            
        for article in articles:
            if len(books_data) >= min_books:
                break
                
            link_tag = article.find("h3").find("a")
            if not link_tag:
                continue
                
            link = link_tag['href']
            book_url = urljoin(url, link)
            
            print(f"  Scraping book {len(books_data)+1}: {book_url}")
            book_details = scrape_book_details(book_url)
            
            if book_details:
                books_data.append(book_details)
            
            # Delay 1-2 seconds
            time.sleep(2)
            
        page += 1
        time.sleep(1) # Delay between pages

    return books_data

def save_to_csv(data, filename):
    keys = ["Title", "Price", "Rating", "Category", "Availability"]
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"Saved {len(data)} records to {filename}")

if __name__ == "__main__":
    data = scrape_catalogue(MIN_BOOKS)
    save_to_csv(data, OUTPUT_FILE)
