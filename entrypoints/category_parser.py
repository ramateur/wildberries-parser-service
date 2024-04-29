import argparse

from src.logging import setup_file_logger
from src.parser.parser import WildberriesParser


def main():
    parser = argparse.ArgumentParser(description='Parse a specific category and page number')
    parser.add_argument('category_link', type=str, help='The category link to parse')
    parser.add_argument('--pages_count', type=int, default=1, help='The page number to parse (default 1)')
    parser.add_argument('--offset_page', type=int, default=1, help='Offset page number (default 1)')
    args = parser.parse_args()

    # setup logging
    setup_file_logger()

    wb_parser = WildberriesParser()
    wb_parser.parse_category(
        category_link=args.category_link, pages_count=args.pages_count, offset_page=args.offset_page
    )


if __name__ == '__main__':
    main()
