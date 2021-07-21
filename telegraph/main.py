# program to scrape the contents of The Telegraph 

import requests
from requests import get
from bs4 import BeautifulSoup
import json
import re
import numpy as np

# array of all articles
final_list = []

for i in range(25):
    url = "https://www.telegraph.co.uk/brexit/" + "page-" + str(i+1)
    response = requests.get(url, timeout = 5)
    content = BeautifulSoup(response.text, "html.parser")
    #initialize empty array of links on the page
    URL = []
    URL_strings = []

    article = content.find_all('div', class_='card__content')

    for link in article:
        #gather list of all URLs on page
        if link.a['href'] not in URL:
            URL.append(link.a['href'])

    #creating the array of URLs
    for i in URL:
        URL_strings.append("https://telegraph.co.uk" + str(i))

    print(URL_strings)
    print("\n\n")

    for i in URL_strings:
        url_2 = str(i)
        response_2 = requests.get(url_2, timeout = 5)
        content_2 = BeautifulSoup(response_2.text, "html.parser")

        # initialize empty strings for heading and body for every new article
        headings = ""
        text = ""
        main_content = content_2.find_all('div', class_='main-content')
        main_content_format_2 = content_2.find_all('article', class_='grid')

        for elem in main_content:
            # heading
            heading = elem.find('h1', attrs={"class": "headline__heading"})
            if heading == None:
                break
            headings += heading.text

            # content
            article_content = elem.find('div', attrs={"class": "articleBodyText version-2 section"})
            if article_content == None:
                article_content = elem.find('div', attrs={"class": "inlineContent version-1 section"})
                if article_content == None:
                    break
            for para in article_content.find_all('p'):
                text += para.text + " "

            # news object
            newsObject = {
                "head": headings,
                "body": text
            }

            print(newsObject)
            final_list.append(newsObject)

        # checking if page is in different format
        for elem_format_2 in main_content_format_2:
            heading = elem_format_2.find('h1', attrs={"class": "e-headline u-heading-1"})
            if heading != None:
                headings += heading.text
            else:
                heading = elem_format_2.find('h1', attrs={"class": "e-headline u-heading-1 article-comment__header"})
                if heading == None:
                    heading = elem_format_2.find('h1', attrs={"class": "e-headline u-heading-1 article-review__header"})
                if heading == None:
                    break ;
                headings += heading.text

            article_content = elem_format_2.find('div', attrs={"class": "component article-body-text"})
            if article_content != None:
                for para in article_content.find_all('p'):
                    text += para.text + " "
            else:
                article_content = elem_format_2.find('div', attrs={"class": "component article-body-text article-body-text--drop-cap article-body-text--drop-cap-comment"})
                if article_content == None:
                    article_content = elem_format_2.find('div', attrs={"class": "inlineContent version-1 section"})
                if article_content == None:
                    break ;
                for para in article_content.find_all('p'):
                    text += para.text + " "

            # creating a news object
            newsObject = {
                "head": headings,
                "body": text
            }

            print(newsObject)
            final_list.append(newsObject)

# writing the data to .json file for said outlet
with open('telegraph/articleData_telegraph.json', 'w', encoding='utf-8') as outfile:
    json.dump(final_list, outfile, ensure_ascii=False)
