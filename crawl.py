from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag


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

def normailize_urls(links: list, base_url: str) -> list:
    absolute_links = []

    for link in links:
        if link.startswith(base_url):
            absolute_links.append(link)
        else:
            absolute_links.append(urljoin(base_url, link))
    
    return absolute_links


def get_urls_from_html(html, base_url):
    '''
    html is an HTML string
    base_url is the root URL of the website we're crawling
    It returns an un-normalized list of all the URLs found within the HTML, or an error if one occurs.
    '''
    soup = BeautifulSoup(html, features = "html.parser")
    a_tags = soup.find_all("a")
    links = []
    for tag in a_tags:
        # print(tag.attrs)
        if "href" in tag.attrs:
            links.append(tag.attrs["href"])
    
    '''
    absolute_links = []

    for link in links:
        if link.startswith(base_url):
            absolute_links.append(link)
        else:
            absolute_links.append(urljoin(base_url, link))
    
    return absolute_links
    '''
    return normailize_urls(links, base_url)

def get_images_from_html(html, base_url):
    '''
    html is an HTML string
    base_url is the root URL of the website we're crawling
    Returns an un-normalized list of all the image URLs found within the HTML, and an error if one occurs.
    '''
    soup = BeautifulSoup(html, "html.parser")
    imgs = soup.find_all("img")
    print(imgs)
    output = []
    for img in imgs:
        output.append(img.get("src"))
    
    return normailize_urls(output, base_url)


