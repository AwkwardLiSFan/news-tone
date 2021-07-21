# importing the necessary packages
import requests
from requests import get
from bs4 import BeautifulSoup
import json
import re
import numpy as np

# array of all articles
final_list = []

# getting the first 100 pages of Brexit articles from The Guardian's Brexit page
for i in range(100):
    # Brexit pages of The Guardian follow the below url structure
    url = "https://www.theguardian.com/politics/eu-referendum" + "?page=" + str(i+1)
    response = requests.get(url, timeout = 5)
    content = BeautifulSoup(response.text, "html.parser")

    # initialize empty array of links on the page
    URL = []
    URL_strings = []

    article = content.find_all('div', class_='fc-item__container')

    for link in article:
        # gather list of all URLs on page
        if link.a['href'] not in URL:
            URL.append(link.a['href'])

    # creating the array of URLs
    for i in URL:
        URL_strings.append(str(i))

    print(URL_strings)
    print("\n\n")

    for i in URL_strings:
        url_2 = str(i)
        response_2 = requests.get(url_2, timeout = 5)
        content_2 = BeautifulSoup(response_2.text, "html.parser")

        # initialize empty strings to store the heading and body for every
        # new article
        headings = ""
        text = ""
        main_content = content_2.find_all('div', class_='css-7i96d9')
        main_content_format_2 = content_2.find_all('div', class_='gs-container')

        for elem in main_content:
            # heading
            heading = elem.find('h1', attrs={"class": "css-rtdfvn"})
            if heading == None:
                heading = elem.find('h1', attrs={"class": "css-s74cjb"})
                if heading == None:
                    heading = elem.find('h1', attrs={"class": "css-rxpjzd"})
                    if heading == None:
                        heading = elem.find('h1', attrs={"class": "hcontent__headline"})
                        if heading == None:
                            break
            headings += heading.text

            # content
            article_content = elem.find('div', attrs={"class": "css-avj6db"})
            if article_content == None:
                article_content = elem.find('div', attrs={"class": "css-1tvz1d9"})
                if article_content == None:
                    article_content = elem.find('div', attrs={"class": "article-body-commercial-selector css-79elbk"})
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

        # checking to see if page is in different format
        for elem_format_2 in main_content_format_2:
            heading = elem_format_2.find('h1', attrs={"class": "content__headline"})
            if heading != None:
                headings += heading.text
            else:
                heading = elem_format_2.find('h1', attrs={"class": "content__headline content__headline--no-margin-bottom"})
                if heading == None:
                    break ;
                headings += heading.text

            article_content = elem_format_2.find('div', attrs={"class": "content__article-body from-content-api js-article__body"})
            if article_content != None:
                for para in article_content.find_all('p'):
                    text += para.text + " "
            else:
                article_content = elem_format_2.find('div', attrs={"class": "component article-body-text article-body-text--drop-cap article-body-text--drop-cap-comment"})
                if article_content == None:
                    break ;
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
with open('guardian/articleData_Guardian.json', 'w', encoding='utf-8') as outfile:
    json.dump(final_list, outfile, ensure_ascii=False)
