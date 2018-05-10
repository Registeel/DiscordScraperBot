import discord
from lxml import html
import requests
import random
import config as cfg
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebKit import *
from discord.ext.commands import Bot
from discord.ext import commands

Client = discord.Client()
bot_prefix= "~"
client = commands.Bot(command_prefix=bot_prefix)
continuePrices = False
currentItem = 0

class Render(QWebPage):  
  def __init__(self, url):  
    self.app = QApplication(sys.argv)  
    QWebPage.__init__(self)  
    self.loadFinished.connect(self._loadFinished)  
    self.mainFrame().load(QUrl(url))  
    self.app.exec_()  
  
  def _loadFinished(self, result):  
    self.frame = self.mainFrame()  
    self.app.quit()

@client.event
async def on_ready():
	print("Bot Online!")
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
	await client.say("I got nuffin")

@client.command(pass_context=True)
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
    url = 'https://pubgtracker.com/profile/pc/Fuzzyllama/duo?region=na'
    r = Render(url)
    result = r.frame.toHtml()
    archive_links = html.fromstring(str(result.toAscii()))

    page = requests.get('https://pubgtracker.com/profile/pc/Fuzzyllama/duo?region=na')
    tree = html.fromstring(page.content)
    duoRank = tree.xpath('//span[@class="value"]/text()')
    print(duoRank)
    #await client.say("Chris' rank in Duos is " + duoRank)

client.run(cfg.token['token'])

