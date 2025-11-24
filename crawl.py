from urllib.parse import urlparse, urljoin

import requests
from bs4 import BeautifulSoup


def normalize_url(url_string):
    if not url_string:
        return None
    parse_result = urlparse(url_string)
    return f"{parse_result.netloc}{parse_result.path}".lower()


def get_h1_from_html(html):
    soup = BeautifulSoup(html, "lxml")
    h1_title = soup.find("h1")
    if not h1_title:
        return ""
    return h1_title.get_text()


def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, "lxml")
    paragraph = soup.find("p")
    if not paragraph:
        return ""
    return paragraph.get_text()


def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, "lxml")
    a_tags = soup.find_all("a", href=True)
    urls = []
    for a in a_tags:
        href = a["href"]
        if href.startswith("http"):
            urls.append(href)
        else:
            absolute_url = urljoin(base_url, href)
            urls.append(absolute_url)
    return urls


def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html, "lxml")
    img_tags = soup.find_all("img", src=True)
    urls = []
    for img in img_tags:
        href = img["src"]
        if href.startswith("http"):
            urls.append(href)
        else:
            absolute_url = urljoin(base_url, href)
            urls.append(absolute_url)
    return urls


def extract_page_data(html, page_url):
    return {
        "url": page_url,
        "h1": get_h1_from_html(html),
        "first_paragraph": get_first_paragraph_from_html(html),
        "outgoing_links": get_urls_from_html(html, page_url),
        "image_urls": get_images_from_html(html, page_url),
    }


def get_html(url):
    response = requests.get(url=url, headers={"User-Agent": "BootCrawler/1.0"})
    response.raise_for_status()

    if "text/html" not in response.headers.get("content-type"):
        raise Exception("Response content type is not 'text/html'")

    return response.text


def safe_get_html(url):
    try:
        return get_html(url)
    except Exception as e:
        print(f"{e}")
        return None


def crawl_page(base_url, current_url=None, page_data=None):
    if current_url is None:
        current_url = base_url

    if page_data is None:
        page_data = {}

    base_url_obj = urlparse(base_url)
    current_url_obj = urlparse(current_url)
    if current_url_obj.netloc != base_url_obj.netloc:
        return page_data

    normalized_url = normalize_url(current_url)

    if normalized_url in page_data:
        print(f"[INFO] Skipping already crawled: {normalized_url}")
        return page_data

    print(f"[INFO] Scraping page: {current_url}")

    html = safe_get_html(current_url)
    if html is None:
        return page_data

    page_info = extract_page_data(html, current_url)
    page_data[normalized_url] = page_info

    next_urls = get_urls_from_html(html, base_url)

    for next_url in next_urls:
        page_data = crawl_page(base_url, next_url, page_data)

    return page_data
