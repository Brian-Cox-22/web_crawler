from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
from typing import TypedDict
import requests
# from typing import Optional


def normalize_url(url):
    parsed_url = urlsplit(url)
    full_path = f"{parsed_url.netloc}{parsed_url.path}"
    full_path = full_path.rstrip("/")
    return full_path.lower()

def get_heading_from_html(html: str) -> str:
    '''
    Finds the h1 (if present). IF no h1, finds h2. IF neighter are present, returns an empty str
    '''
    soup: Tag = BeautifulSoup(html, features="html.parser")
    try:
        try: return soup.h1.get_text(strip=True)
        except: return soup.h2.get_text(strip=True)
    except:
        return ""

def get_first_paragraph_from_html(html: str) -> str:
    '''
    Should return the first <p> tag in the document
    '''
    soup = BeautifulSoup(html, features="html.parser")
    try:
        try:
            return soup.main.p.get_text(strip=True)
        except:
            return soup.p.get_text(strip=True)
    except:
        return ""




def get_urls_from_html(html: str, base_url: str) -> list[str]:
    '''
    Takes a passage of html (as a str), and a base url (of the website)
    Returns a list of strings of valid links, including the base_url
    '''
    urls = []
    soup = BeautifulSoup(html, "html.parser")
    anchors = soup.find_all("a")

    for anchor in anchors:
        if not isinstance(anchor, Tag):
            continue
        href = anchor.get("href")
        if isinstance(href, str) and href:
            try:
                absolute_url = urljoin(base_url, href)
                urls.append(absolute_url)
            except Exception as e:
                print(f"{str(e)}: {href}")

    return urls


def get_images_from_html(html: str, base_url: str) -> list[str]:
    '''
    Takes a passage of html (as a str), and a base url (of the website)
    Returns a list of strings of valid links to images, including the base_url
    Searches based on the src tag in img objects
    '''
    image_urls = []
    soup = BeautifulSoup(html, "html.parser")
    images = soup.find_all("img")

    for img in images:
        if not isinstance(img, Tag):
            continue
        src = img.get("src")
        if isinstance(src, str) and src:
            try:
                absolute_url = urljoin(base_url, src)
                image_urls.append(absolute_url)
            except Exception as e:
                print(f"{str(e)}: {src}")

    return image_urls

class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]


def extract_page_data(html: str, page_url: str):
    '''
    html is an HTML string
    page_url is the absolute URL of the page (used for converting relative URLs)
    It returns a dictionary with keys: url, heading, first_paragraph, outgoing_links, image_urls
    '''
    
    output = PageData(url=page_url, heading=get_heading_from_html(html),
                      first_paragraph=get_first_paragraph_from_html(html),
                      outgoing_links=get_urls_from_html(html, page_url),
                      image_urls=get_images_from_html(html, page_url))

    return output

def get_html(url):
    try:
        response = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    except Exception as e:
        raise Exception(f"network error while fetching {url}: {e}")

    if response.status_code > 399:
        raise Exception(f"got HTTP error: {response.status_code} {response.reason}")

    content_type = response.headers.get("content-type", "")
    if "text/html" not in content_type:
        raise Exception(f"got non-HTML response: {content_type}")

    return response.text


def safe_get_html(url: str) -> str | None:
    try:
        return get_html(url)
    except Exception as e:
        print(f"{e}")
        return None


def crawl_page(
    base_url: str,
    current_url: str | None = None,
    page_data: dict[str, PageData] | None = None,
) -> dict[str, PageData]:
    if current_url is None:
        current_url = base_url
    if page_data is None:
        page_data = {}

    base_url_obj = urlsplit(base_url)
    current_url_obj = urlsplit(current_url)
    if current_url_obj.netloc != base_url_obj.netloc:
        return page_data

    normalized_url = normalize_url(current_url)

    if normalized_url in page_data:
        return page_data

    print(f"crawling {current_url}")
    html = safe_get_html(current_url)
    if html is None:
        return page_data

    page_info = extract_page_data(html, current_url)
    page_data[normalized_url] = page_info

    next_urls = get_urls_from_html(html, base_url)
    for next_url in next_urls:
        page_data = crawl_page(base_url, next_url, page_data)

    return page_data