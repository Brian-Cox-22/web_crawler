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


def get_urls_from_html(html, base_url):
    '''
    html is an HTML string
    base_url is the root URL of the website we're crawling
    It returns an un-normalized list of all the URLs found within the HTML, or an error if one occurs.
    '''

    '''
    Structure:
        relative url->absolute url (add base_url)
    
    need to find all of the <a> tags (use .find_all() method from BeautifulSoup)
    
    '''
    soup = BeautifulSoup(html, features = "html.parser")
    a_tags = soup.find_all("a")
    links = []
    for tag in a_tags:
        # print(tag.attrs)
        if "href" in tag.attrs:
            links.append(tag.attrs["href"])
    
    absolute_links = []

    for link in links:
        if link.startswith(base_url):
            absolute_links.append(link)
        else:
            absolute_links.append(urljoin(base_url, link))
    
    # print(absolute_links)
    return absolute_links