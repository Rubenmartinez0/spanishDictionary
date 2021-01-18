import asyncio
import telepot
import telepot.aio
from telepot.aio.loop import MessageLoop
import requests # library for HTTP requests
from pprint import pprint # library to prettify our debug logs
from bs4 import BeautifulSoup # Library to parse HTML pages
import re

# Modifiable function
async def handle(msg):
    global chat_id
    # These are some useful variables
    content_type, chat_type, chat_id = telepot.glance(msg)
    # Log variables
    print(content_type, chat_type, chat_id)
    pprint(msg)
    username = msg['chat']['first_name']

    if content_type == 'text': # Check that the content type is text 
        if msg['text'] != '/start': # Check that the content is not the starting command
            if msg['text'] == '/pdd':
                await getWotdMeaning()
            else:
                text = msg['text']
                text = text.strip() 
                await getMeaning(text.lower())
                

async def addHeaderStr(number, word):
    if number > 1:
        headerStr = '*Definiciones de '
    elif number == 1:
        headerStr = '*Definición de '
    headerStr += word + ':*\n'
    return headerStr

async def getMeaning(word):
    url = 'https://dle.rae.es/' + word  # Create url
    page = requests.get(url) # Get whole page
    soup = BeautifulSoup(page.text, 'html.parser') # parse HTML response

    try:
        definitions = [] # Iniciate an array
        for element in soup.find_all("p", class_="j"): # Webscrap for html elements that have specified properties.
            #elementDefinition = re.sub('\d. *.. ', '', elementDefinition)
            elementDefinition = element.get_text()
            definitions.append(elementDefinition) # Add element to array.
        if(len(definitions) == 0): # Check if any definition was found.
            suggestionWord = soup.find('a', {'data-cat': 'FETCH', 'data-acc': 'LISTA APROX'}).text # Look if pages suggest a word.
            if(suggestionWord):
                responseStr = 'La palabra "' + word + '" no está en el Diccionario.'
                if(suggestionWord[-1].isdigit()): # In order to avoid infinite loops.
                    await bot.sendMessage(chat_id, responseStr)
                else:
                    responseStr += ' La palabra "' + suggestionWord +'" podría estar relacionada.'
                    await bot.sendMessage(chat_id, responseStr)
                    await getMeaning(suggestionWord)
            else:
                responseStr = '*La palabra "' + word + '" no está en el Diccionario.*'
                await bot.sendMessage(chat_id, responseStr, parse_mode= 'Markdown')
        else:
            try:
                responseStr = await addHeaderStr(len(definitions), word)
                for e in definitions:
                    responseStr += e + '\n'
                
                await bot.sendMessage(chat_id, responseStr, parse_mode= 'Markdown')
            except:
                await bot.sendMessage(chat_id, 'Error al mostrar la/s definición/es...')
    except:
        await bot.sendMessage(chat_id, 'Significado no encontrado...')

async def getWotdMeaning():
    url = 'https://dle.rae.es/' + "saludo"  # Create url
    page = requests.get(url) # Get whole page
    soup = BeautifulSoup(page.text, 'html.parser') # parse HTML response

    try:
        wotd = soup.find('a', {'data-cat': 'WOTD'}).text # Look if pages suggest a word.

        if(wotd):
            responseStr = "La palabra del día es: " + wotd + "."
            await bot.sendMessage(chat_id, responseStr)
            await getMeaning(wotd)
    except:
        await bot.sendMessage(chat_id, 'La palabra del día no ha sido encontrada...')

        

# Program startup

TOKEN = '1548012361:AAHNfddYGNqcPeNh9Bz-v5NRvT1vxCaWnzE'
bot = telepot.aio.Bot(TOKEN)
loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot, handle).run_forever())
print('Listening ...')

loop.run_forever() # Keep the program running