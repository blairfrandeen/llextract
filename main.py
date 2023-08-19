import sys
import requests
from html2text import html2text

import argparse

parser = argparse.ArgumentParser(description="Extract text from a URL")
parser.add_argument("url", help="The URL to extract text from")

args = parser.parse_args()

response = requests.get(args.url)
response.raise_for_status()

html = response.text
md = html2text(html)

print(md)
