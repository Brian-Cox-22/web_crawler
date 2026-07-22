import sys
from crawl import get_html

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
    print(get_html(url))
    # presumably I start actually crawing the site here

if __name__ == "__main__":
    main()
