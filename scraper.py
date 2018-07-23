import sys
import os
import requests
from re import sub, finditer
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image


def download_file(url, dest_dir, filename=None):
    if(filename is None):
        filename = urlsplit(url).path.split("/")[-1]

    request = requests.get(url)
    image = Image.open(BytesIO(request.content))
    image.save(os.path.join(dest_dir, filename))


def get_file_urls(soup):
    file_urls = []

    # Fixes href errors which may occur
    for anchor in soup.find_all(attrs={'class': 'fileThumb'}):
        file_urls.append(sub("//", "http://", anchor.get('href')))
    return file_urls


def get_filenames(soup):
    filenames = []

    for anchor in soup.find_all(attrs={'class': 'fileText'}):
        filenames.append(anchor.get_text().split(" ")[1])
    return filenames


def main():
    print("┌─────────────────────────────────────────────────────────────────────┐")
    print("│                         SUPER SCRAPER V0.1                          │")
    print("│           Image Scraping Tool built by Steven Karmaniolos           │")
    print("└─────────────────────────────────────────────────────────────────────┘")
    
    if(sys.argv[1] == "page"):
        
        # First argument is the page URL
        url = sys.argv[2]

        # Second is the output directory
        # Either relative path or abs. path
        dest_dir = sys.argv[3]
        print("Downloading images from " + url + " ...")

        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")

        file_urls = get_file_urls(soup)
        filenames = get_filenames(soup)

        for i in range(len(file_urls)):
            print("Downloading file: " + filenames[i])
            download_file(file_urls[i], dest_dir, filenames[i])
        
        print("┌─────────────────────────────────────────────────────────────────────┐")
        print("│             Scrape Completed. Your files are now ready.             │")
        print("└─────────────────────────────────────────────────────────────────────┘")

    else:
        print("Usage: python3 scraper.py <'page' or 'board'> <page url or board letter> <dest directory>")


main()
