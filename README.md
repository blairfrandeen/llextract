# llextract

Simple command line tool for extracting text from webpages to use as context when working with large language models (llms).

## Installation
```
git clone git@github.com:blairfrandeen/llextract
cd llextract
pip install .
```

## Usage
Extract text to STDOUT to use with LLMs. Recommend piping the output to the clipboard or to a text file.
```
llextract https://example.com
```
