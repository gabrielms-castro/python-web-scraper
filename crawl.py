from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import lxml

def normalize_url(url_string):
    if not url_string:
        return None
    parse_result = urlparse(url_string)
    return f"{parse_result.netloc}{parse_result.path}"

def get_h1_from_html(html):
    soup = BeautifulSoup(html, 'lxml')
    h1_title = soup.find('h1')
    if not h1_title:
        return ""
    return h1_title.get_text()

def get_first_paragraph_from_html(html):
    soup = BeautifulSoup(html, 'lxml')
    paragraph = soup.find('p')
    if not paragraph:
        return ""
    return paragraph.get_text()

def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, 'lxml')
    a_tags = soup.find_all('a', href=True)
    urls = []
    for a in a_tags:
        href = a['href']
        if href.startswith('http'):
            urls.append(href)
        else:
            absolute_url = urljoin(base_url, href)
            urls.append(absolute_url)
    return urls

def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html, 'lxml')
    img_tags = soup.find_all('img', src=True)
    urls = []
    for img in img_tags:
        href = img['src']
        if href.startswith('http'):
            urls.append(href)
        else:
            absolute_url = urljoin(base_url, href)
            urls.append(absolute_url)
    return urls

def extract_page_data(html, page_url):
    data = {}
    data['url'] = page_url
    data['h1'] = get_h1_from_html(html)
    data['first_paragraph'] = get_first_paragraph_from_html(html)
    data['outgoing_links'] = get_urls_from_html(html, page_url)
    data['image_urls'] = get_images_from_html(html, page_url)
    return data