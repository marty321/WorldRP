import discord
import os

client = discord.Client()

PREFIX = ".."
TOKEN = "token goes here"

@client.event
async def on_ready():
   print('We have logged in as {0.user}'.format(client))
   
@client.event
async def on_message(message):
    if not message.content.startswith(PREFIX):
        return
    command = message.content[len(prefix):]
    
    if command == 'fish'
      await message.channel.send('Fishing successful!')

    if command == '..farm':
      await message.channel.send('Farming successful!')


client.run(TOKEN)
