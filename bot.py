import discord
import inflect
import config as cfg
from lxml import html
import requests
import random
import config as cfg
import sys
from selenium import webdriver
from discord.ext.commands import Bot
from discord.ext import commands

#Set Client variable for later use
Client = discord.Client()

#This will precede any bot commands in chat
bot_prefix= "~"

#Assign the command prefix from the bot prefix
client = commands.Bot(command_prefix=bot_prefix)
continuePrices = False
currentItem = 0
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')

#Create global variable for ordinal conversion of days (1 to 1st, 2 to 2nd, etc)
global p
#Assign the p variable
p = inflect.engine()
#Array for storing newegg item names from searches
global itemNames
itemNames = []
#Array for storing characteristics (numbers before decimal) of newegg items
global itemCharacteristics
itemCharacteristics = []
#Array for storing mantissas (numbers after decimal) of newegg items
global itemMantissas
itemMantissas = []

#Runs when bot starts
@client.event
async def on_ready():
    #Message prints in the console
	print("Bot Online!")
    #No prices to continue yet
	global continuePrices
	continuePrices = False
    #Set the global for the current item in newegg search
    #Used as an index to check against list length
	global currentItem
    #Set start index of current item
	currentItem = 0

    ####This isn't working for some reason####
	print("Name: ".format(client.user.name))
	print("ID: ".format(client.user.id))

#Basic ping/pong functionality
@client.command(pass_context=True)
async def ping(ctx):
	await client.say("Pong!")


#A function to get history for a given day
#month - the month in full form (january, february, etc)
#day - the day in numeric form (1, 2, 3, etc)
@client.command(pass_context=True)
async def gimmeSomeHistory(ctx, month, *, day):
    #global variable declaration - python is weird
    global p
    #Get the page content from the history url
    page = requests.get('https://www.onthisday.com/events/' + month + "/" + day)
    #Get the xpaths for all of the page content
    tree = html.fromstring(page.content)
    #Get facts from their specified xpath
    facts = tree.xpath('/html/body/main/article/div[*]/ul/li/text()')
    #Get the dates to match the facts
    dates = tree.xpath('/html/body/main/article/div[*]/ul/li/b/a/text()')
    #Get the number of facts scraped
    numFacts = len(facts)
    #If there is more than one fact, we want to randomize the fact we are looking at
    if numFacts > 1:
        #Generate a random number for an item index
        randNum = random.randint(0,numFacts - 1)
        #Print the fact in a readable format
        await client.say("On " + month + " " + p.ordinal(day) + " in " + dates[randNum] + ":" + facts[randNum])
    #If there are no facts then let the user know
    elif numFacts == 0:
        await client.say("No facts for " + month + " " + p.ordinal(day))
    #Catch all if there is some kind of error
    else:
        await client.say("Error getting facts")

#Yes command for continuing list of matches for neweggSearch
@client.command(pass_context=True)
async def Y(ctx):
    #Declare the globals we use
    global continuePrices
    global currentItem
    global itemNames
    global itemCharacteristics
    global itemMantissas
    #If the user wants to continue and the currentItem is in the list
    if continuePrices and currentItem < len(itemNames):
        #Print the item and price
        await client.say("I found " + itemNames[currentItem][0] + "\nfor $" + itemCharacteristics[currentItem][0] + "" + itemMantissas[currentItem][0])
        #Increment the item counter
        currentItem += 1
        #Prompt for next item
        await client.say("Would you like me to show you the next best match? (~Y/~n)")
    #Reached the end of the list
    elif currentItem == len(itemNames):
        await client.say("Last element in search")
        #Do not allow continue
        continuePrices = False
        #Reset item index
        currentItem = 0

#Command to search Newegg for given items
#item - the item to search for (gtx1080, Razer Kraken V2, etc)
@client.command(pass_context=True)
async def searchNewegg(ctx, item, item2="", item3="", item4="", *, item5=""):
    #Declare the globals we need
    global continuePrices
    global currentItem
    global itemNames
    global itemCharacteristics
    global itemMantissas
    #Variable for length of item list
    itemList = 0
    #Declare loop variable
    endCount = 0;
    #Set array for itemNames
    itemNames = []
    #Combine the argument for the item
    itemString = item + "+" + item2 + "+" + item3 + "+" + item4 + "+" + item5
    #Show a combined string to display to user
    itemStringDisplay = item + " " + item2 + " " + item3 + " " + item4 + " " + item5
    #Set the current item to the start of the list
    currentItem = 0
    #Generate the search url
    searchURL = "https://www.newegg.ca/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=" + itemString + "&ignorear=-1&isNodeId=1";
    #Get the page from the url we generated
    page = requests.get(searchURL)
    #Get the html structure for the page
    tree = html.fromstring(page.content)

    #Create the list of all matches
    for x in range(1, 11):
        notExists = not(tree.xpath('//*[@id="bodyArea"]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[2]/div[' + str(x) + ']/div/a/text()'))
        if(not(notExists)):
            checkItem = tree.xpath('//*[@id="bodyArea"]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[2]/div[' + str(x) + ']/div/a/text()')
            checkItem = checkItem[0].strip()
            print("Checkitem " + checkItem[0])
            if(len(checkItem[0]) < 5):
                itemNames.append(tree.xpath('//*[@id="bodyArea"]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[2]/div[' + str(x) + ']/div/a/text()'))
                itemCharacteristics.append(tree.xpath('//li[@class="price-current"]/strong/text()')[x-1])
                itemMantissas.append(tree.xpath('//li[@class="price-current"]/sup/text()')[x-1])

    #Turn on the continue prices
    continuePrices = True
    #Increment the item in the list
    currentItem += 1
    #Get number of items returned from search
    itemList = len(itemNames)

    print(len(itemNames))
    print(len(itemCharacteristics))
    print(len(itemMantissas))

    await client.say("`=========================`")
    await client.say("`=  Results For Search   =`")
    await client.say("`=========================`")
    for x in range(0, len(itemNames)):
        print("item: " + str(len(itemNames[x])))
        print("charac: " + str(len(itemCharacteristics[x])))
        print("mantissa: " + str(len(itemMantissas[x])))
        stringLength = len(itemNames[x][0])
        string = itemNames[x][0]
        counter = 0
        while (counter < stringLength):
            if (stringLength-counter) < 23 and (stringLength-counter) > 0:
                spaceLength = (23 - (stringLength-counter)) + 1
                spaceString = "`="
                for z in range(1, int(spaceLength/2)+1):
                    spaceString += " "
                spaceString += string[(counter):(stringLength)]
                spacesLeft = 26 - len(spaceString)
                print("spacestring " + str(len(spaceString)))
                for a in range(1, spacesLeft):
                    spaceString += " "
                spaceString += "=`"
                await client.say(spaceString)
                counter += (stringLength-counter)
            else:
                counter += 23
                startStringIndex = 0
                if(counter > 23):
                    startStringIndex = counter-23
                printString = (string[startStringIndex:counter])
                await client.say("`=" + printString + "=`")
                itemNames[x] = string[:counter]
        priceLength = len(itemCharacteristics[x]) + len(itemMantissas[x])
        priceWhitespace = 23 - priceLength
        priceString = "`="
        for i in range(1, int(priceWhitespace/2)+1):
            priceString += " "
        priceString += "$" + itemCharacteristics[x] + itemMantissas[x]
        for j in range(1, int(priceWhitespace/2)):
            priceString += " "
        priceString += "=`"
        await client.say(priceString)
        await client.say("`=========================`")

        

async def searchNewegg(ctx, *, item):
    searchURL = "https://www.newegg.ca/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=" + item + "=-1&isNodeId=1";
    page = requests.get(searchURL)
    tree = html.fromstring(page.content)
    firstItemName = tree.xpath('//*[@id="bodyArea"]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/a/text()')
    firstItemCharacteristic = tree.xpath('//*[@id="bodyArea"]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/ul/li[3]/strong/text()')
    firstItemMantissa = tree.xpath('//*[@id="bodyArea"]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/ul/li[3]/sup/text()')
    print(firstItemCharacteristic)
    await client.say("I found " + firstItemName[0] + "\nfor $" + firstItemCharacteristic[0] + "" + firstItemMantissa[0])
	#await client.say("Would you like me to show you the next best match? (Y/n)")
	#currentItem += 1

@client.command(pass_context=True)
async def checkChrisPubg(ctx):
    print("Hit this")
    browser = webdriver.Chrome(chrome_options=options)
    url = 'https://pubgtracker.com/profile/pc/Fuzzyllama/duo?region=na'
    browser.get(url)
    innerHTML = browser.execute_script("return document.body.innerHTML")

    tree = html.fromstring(innerHTML)
    duoRank = tree.xpath('//*[@id="profile"]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/span[2]/text()')

    await client.say("Chris' rank in Pubg Doubles is " + str(duoRank[0]))

    browser.quit()

client.run(cfg.token['token'])

