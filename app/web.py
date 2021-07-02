#https://blog.geekhunter.com.br/como-fazer-um-web-scraping-python/

import sys

from bs4 import BeautifulSoup

import requests

html = requests.get(sys.argv[1]).content

soup = BeautifulSoup(html, 'html.parser')

print(soup.prettify())