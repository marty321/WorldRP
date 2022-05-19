import discord
import os

client = discord.Client()

@client.event
async def on_ready():
 print('We have logged in as {0.user}'.format(client))
@client.event
async def on_message(message):
 if message.content.startswith('..fish'):
  await message.channel.send('Fishing successful!')
client.run(os.getenv('hello'))

 if message.content.startswith('..farm'):
  await message.channel.send('Farming successful!')
client.run(os.getenv('hello'))
