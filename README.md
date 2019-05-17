# Image Board File Scraper

## Methods of Use
- Can be run as a standalone script or through the included Jupyter Notebook.

## Requirements & Dependencies
- python3, pip3
- BeautifulSoup4

## Installation
- Step 1
  - 'sudo pip3 install -r req-list.txt'
- Step 2
  - eg. 'python3 scraper.py page <url> <path>' where url is the webpage you want to scrape and path is the path on your computer. Ensure that the destination directory exists before running.

## Notes
- Fixed issue with inability to download images that are not PNG files;
  ~~~~
  def img_alpha_to_colour(image, color=(255, 255, 255)):
      image.load()  # needed for split()
      background = Image.new('RGB', image.size, color)
      background.paste(image, mask=image.split()[3])  # 3 is the alpha channel
      return background
  ~~~~

- Added jupyter notebook version.
