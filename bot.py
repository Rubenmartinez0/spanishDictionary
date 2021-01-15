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
        if msg['text'] != '/start': # Check that the content is not the starting
            text = msg['text']
            text = text.strip() 
            await getMeaning(text.lower())

    # Send our JSON msg variable as reply message
    #await bot.sendMessage(chat_id, msg)


async def getMeaning(word):
    # create url
    url = 'https://dle.rae.es/' + word
    # get page
    page = requests.get(url)
    # parse HTML response
    soup = BeautifulSoup(page.text, 'html.parser')
    #pprint(soup)
    try:
        try:
            definitions = []
            for element in soup.find_all("p", class_="j"): #Webscrap definitions

                #elementDefinition = re.sub('\d. *.. ', '', elementDefinition)
                #elementDefinition =  re.compile("[A-Z]").split(elementDefinition)[1]# remove characters until MAYUS
                #pprint(element.get_text())
                elementDefinition = element.get_text()
                definitions.append(elementDefinition)
        except:
            await bot.sendMessage(chat_id, 'Meaning not found...')

        try:
            responseStr = ''
            for e in definitions:
                responseStr += e + '\n'

            await bot.sendMessage(chat_id, responseStr)
        except:
            await bot.sendMessage(chat_id, 'Error displaying definition/s')

    except:
        await bot.sendMessage(chat_id, 'Something went wrong...')
        
# Program startup

TOKEN = '1548012361:AAHNfddYGNqcPeNh9Bz-v5NRvT1vxCaWnzE'
bot = telepot.aio.Bot(TOKEN)
loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(bot, handle).run_forever())
print('Listening ...')

# Keep the program running
loop.run_forever()