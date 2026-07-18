from urllib.parse import urlsplit
from bs4 import BeautifulSoup, Tag

# Stubbed for now, but intent is to check if urls are the same, regardless of http vs https and
# inclusion of final /
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