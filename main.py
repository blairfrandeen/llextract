import sys
import requests
from html2text import html2text
import justext

import argparse


def main(args):
    response = requests.get(args.url)
    response.raise_for_status()

    html = response.text

    if args.method == "justext":
        paragraphs = justext.justext(html, justext.get_stoplist("English"))

        for paragraph in paragraphs:
            if not paragraph.is_boilerplate:
                print(paragraph.text)

    elif args.method == "full":
        md = html2text(html)
        print(md)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract text from a URL")
    parser.add_argument("url", help="The URL to extract text from")
    parser.add_argument(
        "--method",
        default="justext",
        choices=["justext", "full"],
        help="Which method to use. \
                'full' uses the html2text library and will generally give the full content of the page. \
                'justext' will attempt to remove menus, headers, and footers to just deliver the content.",
    )

    args = parser.parse_args()

    main(args)
