import argparse
import os
import requests
import time
import sys


import justext
from html2text import html2text
from tabulate import tabulate
from tokenizers import Tokenizer


def extract_text(html: str, method: str) -> str:  # type: ignore
    if method == "justext":
        paragraphs = justext.justext(html, justext.get_stoplist("English"))

        return "\n".join([para.text for para in paragraphs if not para.is_boilerplate])

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


def main(args):
    inputs = []

    # Take piped inputs from stdin
    if not sys.stdin.isatty():
        inputs.append(sys.stdin.read())

    if not inputs and not args.inputs:
        exit(0)

    # For each input, decide if it's a URL to read, a file, or plain text
    for arg in args.inputs:
        if arg.startswith("http"):
            response = requests.get(arg)
            response.raise_for_status()
            html = response.text
            inputs.append(extract_text(html, args.method))
        elif os.path.isfile(arg):
            with open(arg) as fp:
                inputs.append(fp.read())
        else:
            inputs.append(arg)

    if args.stats:
        print_stats("\n".join(inputs))
    else:
        print("\n".join(inputs))


def cli():
    parser = argparse.ArgumentParser(description="Extract text from a URL")
    parser.add_argument("inputs", nargs="*", help="URLs, files, or piped text")
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


if __name__ == "__main__":
    cli()
