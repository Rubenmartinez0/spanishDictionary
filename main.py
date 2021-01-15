import requests # library for HTTP requests
from pprint import pprint # library to prettify our debug logs
from bs4 import BeautifulSoup # Library to parse HTML pages
import re

def getMeaning(word):
    # create url
    url = 'https://dle.rae.es/' + word
    # get page
    page = requests.get(url)
    # parse HTML response
    soup = BeautifulSoup(page.text, 'html.parser')
    #pprint(soup)

    try:
        #get definitions
        definitions = []
        #definitions = soup.find('p', {'class': 'j'}).text
        #pprint(definitions)
        for element in soup.find_all("p", class_="j"):

            #elementDefinition = re.sub('\d. *.. ', '', elementDefinition)
            #elementDefinition =  re.compile("[A-Z]").split(elementDefinition)[1]# remove characters until MAYUS
            #pprint(element.get_text())
            
            elementDefinition = element.get_text()
            definitions.append(elementDefinition)
    except:
        pprint('Meaning not found..')

    for e in definitions:
        pprint(e)

word = 'tren'
word = word.strip() # remove both leading and trailing blank/space characters 
getMeaning(word.lower())


