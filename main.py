import os
import discord
import requests
import json
import datetime

client = discord.Client() 

def get_quote(stock_ticker):
  url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=' + stock_ticker + '&apikey=' + os.getenv('APIKEY')
  r = requests.get(url)
  data = r.json()

  latest_data = data['Meta Data']["3. Last Refreshed"]
  print(latest_data)
  highprice = data['Time Series (Daily)'][latest_data]['2. high']
  lowprice = data['Time Series (Daily)'][latest_data]['3. low']
  return highprice, lowprice, latest_data

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$boo'):
    await message.channel.send('The robot takeover is happening')

  if message.content.startswith('/'):
    stock_ticker_input = message.content.split('/',1)[1]
    latest_price = get_quote(stock_ticker_input)
    pretty_date = datetime.datetime.strptime(latest_price[2], '%Y-%m-%d').strftime('%b %d')
    message_send = "For " + stock_ticker_input + " on " + pretty_date + "\nThe high price is $" + latest_price[0] + "\nThe low price is $" + latest_price[1]
    await message.channel.send(message_send)

client.run(os.getenv('TOKEN'))
