import sys
from crawl import crawl_page


def main():
    args = sys.argv
    if len(args) < 2:
        print("no website provided. Usage: uv run main.py <BASE_URL>")
        sys.exit(1)

    if len(args) > 2:
        print("too many arguments provided")
        sys.exit(1)

    BASE_URL = args[1]
    print(f"[INFO] starting crawl of: {BASE_URL}")
    try:
        page_data = crawl_page(BASE_URL)

        print(f"Found {len(page_data)} pages:")
        for page in page_data.values():
            print(f"- {page['url']}: {len(page['outgoing_links'])} outgoing links")

    except Exception as err:
        print(f"[ERROR] Error fetching {BASE_URL}")


if __name__ == "__main__":
    main()
