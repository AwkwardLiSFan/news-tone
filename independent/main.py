#  this program scrapes the articles off the website

# importing the necessary packages
import requests
from requests import get
from bs4 import BeautifulSoup
import json
import re
import numpy as np

# array of all articles
final_list = []

# getting all Brexit articles from The Independent's Brexit page
url = "https://www.independent.co.uk/topic/brexit"
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout = 5)
content = BeautifulSoup(response.text, "html.parser")

# initialize empty array of links on the page
URL = []
URL_strings = []

article = content.find_all('div', class_='sc-ptdsS ljCfTK image-wrap')

for link in article:
    # gather list of all URLs on page
    if link.a['href'] not in URL:
        URL.append(link.a['href'])

print(URL)
print("\n\n")

for i in URL:
    url_2 = "https://www.independent.co.uk" + str(i)
    response_2 = requests.get(url_2, headers={'User-Agent': 'Mozilla/5.0'}, timeout = 5)
    content_2 = BeautifulSoup(response_2.text, "html.parser")

    # initialize empty strings to store the heading and body for every
    # new article
    headings = ""
    text = ""
    main_content = content_2.find_all('article', class_='sc-pcJBx gkirqO')

    for elem in main_content:
        # heading
        heading = elem.find('h1', attrs={"class": "sc-qQkqj cdfpMG"})
        if heading == None:
            break
        headings += heading.text

        # content
        article_content = elem.find('div', attrs={"class": "sc-qPlDB bUMNyJ"})
        if article_content == None:
            break
        for para in article_content.find_all('p'):
            text += para.text + " "

        # news object
        newsObject = {
            "head": headings,
            "body": text
        }

        # adding the heading + article to the final list
        print(newsObject)
        final_list.append(newsObject)

# writing the data to a .json file
with open('independent/articleData_Independent.json', 'w', encoding='utf-8') as outfile:
    json.dump(final_list, outfile, ensure_ascii=False)
