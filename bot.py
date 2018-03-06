import discord
from lxml import html
import requests
import random
from discord.ext.commands import Bot
from discord.ext import commands

Client = discord.Client()
bot_prefix= "~"
client = commands.Bot(command_prefix=bot_prefix)
itemNames = []
itemCharacteristics = []
itemMantissas = []

@client.event
async def on_ready():
	print("Bot Online!")
	global continuePrices
	continuePrices = False
	global currentItem
	currentItem = 0
	print("Name: ()".format(client.user.name))
	print("ID: ()".format(client.user.id))


@client.command(pass_context=True)
async def ping(ctx):
	continuePrices = False
	await client.say("Pong!")

@client.command(pass_context=True)
async def gimmeSomeHistory(ctx, month, *, day):
	continuePrices = False
	page = requests.get('https://www.onthisday.com/events/' + month + "/" + day)
	tree = html.fromstring(page.content)
	facts = tree.xpath('/html/body/main/article/div[1]/ul/li/text()')
	dates = tree.xpath('/html/body/main/article/div[1]/ul/li/b/a/text()')
	numFacts = len(facts)
	if numFacts > 1:
		randNum = random.randint(0,numFacts)
		await client.say("On " + month + " " + day + " in " + dates[randNum] + ":" + facts[randNum])
	else:
		await client.say("On " + month + " " + day + " in " + dates[0] + ":" + facts[0])

@client.command(pass_context=True)
async def Y(ctx):
	global continuePrices
	global currentItem
	if continuePrices and currentItem < len(itemNames):
		await client.say("I found " + itemNames[currentItem][0] + "\nfor $" + itemCharacteristics[currentItem][0] + "" + itemMantissas[currentItem][0])
		currentItem += 1
		await client.say("Would you like me to show you the next best match? (Y/n)")
	elif currentItem == len(itemNames):
		await client.say("End of top ten elements in search")
		continuePrices = False
		currentItem = 0

@client.command(pass_context=True)
async def searchNewegg(ctx, *, item):
	global continuePrices
	global currentItem
	currentItem = 0
	continuePrices = False
	searchURL = "https://www.newegg.ca/Product/ProductList.aspx?Submit=ENE&DEPA=0&Order=BESTMATCH&Description=" + item + "=-1&isNodeId=1";
	page = requests.get(searchURL)
	tree = html.fromstring(page.content)
	#itemNames.append(tree.xpath('//*[@id="bodyArea"]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/a/text()'))
	#itemCharacteristics.append(tree.xpath('//*[@id="bodyArea"]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/ul/li[3]/strong/text()'))
	#itemMantissas.append(tree.xpath('//*[@id="bodyArea"]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[2]/div[1]/div/div[2]/ul/li[3]/sup/text()'))

	for x in range(1, 11):
		itemNames.append(tree.xpath('//*[@id="bodyArea"]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[2]/div[' + str(x) + ']/div/a/text()'))
		itemCharacteristics.append(tree.xpath('//*[@id="bodyArea"]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[2]/div[' + str(x) + ']/div/div[2]/ul/li[3]/strong/text()'))
		itemMantissas.append(tree.xpath('//*[@id="bodyArea"]/section/div/div/div[2]/div/div/div/div[2]/div[1]/div[2]/div[2]/div[' + str(x) + ']/div/div[2]/ul/li[3]/sup/text()'))

	continuePrices = True
	currentItem += 1
	await client.say("I found " + itemNames[0][0] + "\nfor $" + itemCharacteristics[0][0] + "" + itemMantissas[0][0])
	await client.say("Would you like me to show you the next best match? (~Y/~n)")


client.run("NDIwMzgzNTY3ODAyMTM4NjM0.DX94Yg.AIdFIqAwx1jKRQTTVFXzMyoSd1E")

