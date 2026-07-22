import sys
from crawl import crawl_page

def main():

    # Check that the num of arguments is right: 
    num_arguments = len(sys.argv)
    if num_arguments < 2:
        print("no website provided")
        sys.exit(1)

    if num_arguments > 2:
        print("too many arguments provided")
        sys.exit(1)
    
    url = sys.argv[1]
    print(f"starting crawl at {url}")
    
    
    page_data = crawl_page(url)

    print(f"Found {len(page_data)} pages:")
    for page in page_data.values():
        print(f"- {page['url']}: {len(page['outgoing_links'])} outgoing links")
    
if __name__ == "__main__":
    main()
