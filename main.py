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
    
    
    pages = crawl_page(url) # this will return a dict
    print(f"Number of pages visited: {len(pages)}")
    for page in pages:
        print(page)

    
if __name__ == "__main__":
    main()
