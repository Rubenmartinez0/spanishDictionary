import requests # library for HTTP requests
from pprint import pprint # library to prettify our debug logs
from bs4 import BeautifulSoup # Library to parse HTML pages
import re


def addHeaderStr(number, word):
    if number > 1:
        responseStr = '*Definiciones de '
    elif number == 1:
        responseStr = '*Definición de '
    responseStr += word + ':*\n'
    return responseStr

def getMeaning(word):
    url = 'https://dle.rae.es/' + word
    page = requests.get(url) # Get page from url
    soup = BeautifulSoup(page.text, 'html.parser') # Parse HTML response

    try:
        try:
            definitions = []
            for element in soup.find_all("p", class_="j"):
                #elementDefinition = re.sub('\d. *.. ', '', elementDefinition)
                #elementDefinition =  re.compile("[A-Z]").split(elementDefinition)[1]# remove characters until MAYUS
                #pprint(element.get_text())
                elementDefinition = element.get_text()
                definitions.append(elementDefinition)
            if(len(definitions) == 0):
                # look for suggestion
                suggestionWord = soup.find('a', {'data-cat': 'FETCH', 'data-acc': 'LISTA APROX'}).text
                if(suggestionWord):
                    pprint('La palabra "' + word + '" no está en el Diccionario. La palabra "' + suggestionWord +'" podría estar relacionada: ')
                    getMeaning(suggestionWord)
                else:
                    pprint('La palabra "' + word + '" no está en el Diccionario.')
            else:
                try:
                    responseStr = addHeaderStr(len(definitions), word)
                    for e in definitions:
                        responseStr += e + '\n'
                    
                    pprint(responseStr)
                except:
                    pprint('Error displaying definition/s')
        except:
            pprint('Meaning not found...')
    except:
       pprint('Something went wrong...')




word = 'agaporni'
word = word.strip() # remove both leading and trailing blank/space characters 
getMeaning(word.lower())


