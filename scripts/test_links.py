import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys

BASE_URL = "http://localhost:8080"  # Change to your running app's base URL

visited = set()
broken_links = []

def is_internal(url):
    return url.startswith(BASE_URL) or url.startswith("/")

def crawl(url):
    if url in visited or not is_internal(url):
        return
    full_url = urljoin(BASE_URL, url)
    visited.add(full_url)
    try:
        resp = requests.get(full_url, timeout=10)
    except Exception as e:
        broken_links.append((full_url, f"Request error: {e}"))
        return
    if resp.status_code >= 400:
        broken_links.append((full_url, f"Status {resp.status_code}"))
        return
    soup = BeautifulSoup(resp.text, "html.parser")
    for link in soup.find_all("a", href=True):
        href = link["href"]
        # Ignore mailto, tel, javascript, etc.
        if href.startswith("mailto:") or href.startswith("tel:") or href.startswith("javascript:"):
            continue
        next_url = urljoin(full_url, href)
        # Only crawl internal links
        if urlparse(next_url).netloc == urlparse(BASE_URL).netloc:
            crawl(next_url)

if __name__ == "__main__":
    print(f"Starting crawl at {BASE_URL}")
    crawl(BASE_URL)
    print("\nBroken links found:")
    for url, reason in broken_links:
        print(f"{url} -> {reason}")
    print(f"\nChecked {len(visited)} pages, found {len(broken_links)} broken links.")