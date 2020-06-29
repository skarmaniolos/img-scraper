import sys
import os
import requests
from re import sub, finditer
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image


# gets img from url and save to destination
def download_file(url, dest_dir, filename=None):
    if(filename is None):
        filename = urlsplit(url).path.split("/")[-1]
        
    request = requests.get(url)
    image = Image.open(BytesIO(request.content))
    
    if image.mode in ('RGBA', 'LA'):
        #background = Image.new(image.mode[:-1], image.size, fill_color)
        #background.paste(image, image.split()[-1])
        background = img_alpha_to_colour(image)
        image = background
    
    image.save(os.path.join(dest_dir, filename))

    
# handles img that have no alpha layer 
def img_alpha_to_colour(image, color=(255, 255, 255)):
    image.load()  # needed for split()
    background = Image.new('RGB', image.size, color)
    background.paste(image, mask=image.split()[3])  # 3 is the alpha channel
    return background
    
    
# takes html as input, creates list, appends img elements to list
def get_file_urls(soup):
    file_urls = []
    
    # fix href errors
    for anchor in soup.find_all(attrs={'class':'fileThumb'}):
        file_urls.append(sub("//", "https://", anchor.get('href')))
    return file_urls
    

# iterate through posts, find img filenames
def get_filenames(soup):
    filenames = []

    for anchor in soup.find_all(attrs={'class': 'fileText'}):
        filenames.append(anchor.get_text().split(" ")[1])
        print(filenames.append(anchor.get_text().split(" ")[1]))
    return filenames


# primary function
def main(url):
    print("┌─────────────────────────────────────────────────────────────────────┐")
    print("│           Image Scraping Tool built by Steven Karmaniolos           │")
    print("└─────────────────────────────────────────────────────────────────────┘")
    print("Downloading images from " + url + " ...")
    
    dest_dir = os.getcwd()+'/scraped_imgs'
    
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")

    file_urls = get_file_urls(soup)
    filenames = get_filenames(soup)

    for i in range(len(file_urls)):
        print("Downloading file: " + filenames[i])
        download_file(file_urls[i], dest_dir, filenames[i])

    print("┌─────────────────────────────────────────────────────────────────────┐")
    print("│             Scrape completed. Your files are now ready.             │")
    print("└─────────────────────────────────────────────────────────────────────┘")


main()
