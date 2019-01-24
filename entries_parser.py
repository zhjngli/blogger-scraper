#!/usr/bin/env python
import argparse
from lxml import etree
from bs4 import BeautifulSoup
import csv

def word_count(unicode):
    return len(unicode.encode('ascii', 'replace').split())

def parse_entries(entries_file):
    ef = open(entries_file)
    soup = BeautifulSoup(ef, "lxml")

    csvfile = open('entries.csv', 'wb')
    fieldnames = ['title', 'wordcount', 'datetime']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    entries = soup.find_all('entry')
    for entry in entries:
        title = entry.find_all('title')[0].get_text()
        content = entry.find_all('content')[0].get_text()
        date = entry.find_all('published')[0].get_text()
        writer.writerow({'title': title, 'wordcount': word_count(content), 'datetime': date})
        csvfile.flush()

    csvfile.close()
    ef.close()


def main():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("-i", "--input", required=True, action="store", dest="file", help="Input file to parse")
    
    args = args_parser.parse_args()
    parse_entries(args.file)

if __name__ == "__main__":
    main()
