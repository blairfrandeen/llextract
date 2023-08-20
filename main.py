import argparse
import requests
import sys


import justext
from html2text import html2text
from tabulate import tabulate
from tokenizers import Tokenizer


def main(args):
    response = requests.get(args.url)
    response.raise_for_status()

    html = response.text

    text = extract_text(html, args.method)
    if args.stats:
        print_stats(text)
    else:
        print(text)


def extract_text(html: str, method: str) -> str:  # type: ignore
    if method == "justext":
        paragraphs = justext.justext(html, justext.get_stoplist("English"))

        for paragraph in paragraphs:
            if not paragraph.is_boilerplate:
                return paragraph.text

    elif method == "full":
        md = html2text(html)
        return md

    else:
        raise ValueError(f"Invalid method specified: {method}")


def print_stats(text):
    tokenizer = Tokenizer.from_pretrained("bert-base-uncased")
    tokenized = tokenizer.encode(text)

    num_words = len(text.split())
    num_paragraphs = text.count("\n\n") + 1

    bytes_size = sys.getsizeof(text)

    stats = [
        ["Words", f"{num_words:,}"],
        ["Paragraphs", f"{num_paragraphs:,}"],
        ["Bytes", f"{bytes_size:,}"],
        ["Tokens", f"{len(tokenized.tokens):,}"],
    ]

    print(tabulate(stats, headers=["Metric", "Count"], tablefmt="presto"))


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
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Print word count, paragraph count, byte size, and approximate token size.",
    )

    args = parser.parse_args()

    main(args)
