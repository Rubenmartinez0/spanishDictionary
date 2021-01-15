import requests # library for HTTP requests
from pprint import pprint # library to prettify our debug logs
from bs4 import BeautifulSoup # Library to parse HTML pages
import re

async def getMeaning(word):
    url = 'https://dle.rae.es/' + word
    page = requests.get(url) # Get page from url
    soup = BeautifulSoup(page.text, 'html.parser') # Parse HTML response

    try:
        try:
            #CHECK HERE IF WORD EXISTS
            definitions = []
            for element in soup.find_all("p", class_="j"):

                #elementDefinition = re.sub('\d. *.. ', '', elementDefinition)
                #elementDefinition =  re.compile("[A-Z]").split(elementDefinition)[1]# remove characters until MAYUS
                #pprint(element.get_text())
                elementDefinition = element.get_text()
                definitions.append(elementDefinition)
        except:
            pprint('Meaning not found...')

        try:
            responseStr = ''
            for e in definitions:
                responseStr += e + '\n'
            
            pprint(responseStr)
        except:
           pprint('Error displaying definition/s')

    except:
       pprint('Something went wrong...')

word = 'tren'
word = word.strip() # remove both leading and trailing blank/space characters 
getMeaning(word.lower())


