import requests
from bs4 import BeautifulSoup
import csv
import json
import time

BASE_URL = "https://books.toscrape.com/catalogue/"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}


HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"}

def scrape_page(url):
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    books = []
    for article in soup.select("article.product_pod"):
        title = article.h3.a["title"]
        price = article.select_one("p.price_color").text.strip()
        rating_word = article.p["class"][1]
        rating = RATING_MAP.get(rating_word, 0)
        availability = article.select_one("p.availability").text.strip()

        books.append({
            "title": title,
            "price": price,
            "rating": rating,
            "availability": availability,
        })

    next_btn = soup.select_one("li.next a")
    next_url = BASE_URL + next_btn["href"] if next_btn else None

    return books, next_url


def scrape_all(max_pages=5):
    all_books = []
    url = START_URL
    page = 1

    while url and page <= max_pages:
        print(f"Scraping page {page}...")
        books, url = scrape_page(url)
        all_books.extend(books)
        page += 1
        time.sleep(0.5)

    return all_books


def save_csv(books, filename="books.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "price", "rating", "availability"])
        writer.writeheader()
        writer.writerows(books)
    print(f"Saved {len(books)} books to {filename}")


def save_json(books, filename="books.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(books)} books to {filename}")


if __name__ == "__main__":
    books = scrape_all(max_pages=5)
    save_csv(books)
    save_json(books)
    print(f"\nDone! Total books scraped: {len(books)}")
