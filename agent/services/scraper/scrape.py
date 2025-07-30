import requests
from bs4 import BeautifulSoup, element
from urllib.parse import urljoin, urlparse
import os
import time

base_url = "https://www.changiairport.com/in/en.html"
visited = set()

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36"
}

def is_internal_link(link: str) -> bool:
    parsed = urlparse(link)
    return parsed.netloc == "" or parsed.netloc == urlparse(base_url).netloc

def sanitize_path(url: str, ext: str = ".txt") -> str:
    parsed = urlparse(url)
    path = parsed.path.strip("/") or "index"
    filename = path.replace("/", "_")
    return filename + ext

def extract_visible_text(soup: BeautifulSoup) -> str:
    for tag in soup(["script", "style", "noscript", "svg", "meta", "link"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return "\n".join(lines)

def download_pdf(pdf_url: str):
    os.makedirs("pdfs", exist_ok=True)
    filename = sanitize_path(pdf_url, ext=".pdf")
    filepath = os.path.join("pdfs", filename)

    if os.path.exists(filepath):
        print(f"Already downloaded: {filename}")
        return

    try:
        print(f"PDF: {pdf_url}")
        resp = requests.get(pdf_url, headers=headers, timeout=10)
        if resp.ok and resp.headers.get("Content-Type", "").startswith("application/pdf"):
            with open(filepath, "wb") as f:
                f.write(resp.content)
        else:
            print(f"Skipped invalid PDF: {pdf_url}")
    except Exception as e:
        print(f"Error downloading PDF: {e}")

def should_skip_url(url: str) -> bool:
    parsed = urlparse(url)
    return "zh" in parsed.path.lower()

def scrape(url: str):
    if url in visited or should_skip_url(url):
        return
    visited.add(url)

    print(f"Scraping: {url}")
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        content_type = resp.headers.get("Content-Type", "")

        if "application/pdf" in content_type:
            download_pdf(url)
            return

        if "text/html" not in content_type or resp.status_code != 200:
            return

        soup = BeautifulSoup(resp.text, "html.parser")
        visible_text = extract_visible_text(soup)

        if visible_text:
            os.makedirs("visible_text", exist_ok=True)
            filename = sanitize_path(url)
            filepath = os.path.join("visible_text", filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(visible_text)

        for a in soup.find_all("a", href=True):
            if isinstance(a, element.Tag):
                href = a.get("href")
                if not href:
                    continue
                full_url = urljoin(url, str(href).strip())
                if full_url.endswith(".pdf"):
                    download_pdf(full_url)
                elif is_internal_link(full_url):
                    scrape(full_url)

        time.sleep(1)

    except Exception as e:
        print(f"Error scraping {url}: {e}")

scrape(base_url)
