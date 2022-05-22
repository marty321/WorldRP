import disnake
import os

client = disnake.Client()

PREFIX = ".."

tokenFile = open("token.txt","r")
TOKEN = tokenFile.read()
if TOKEN == "":
  raise RuntimeError("No token in token.txt")
tokenFile.close()

@client.event
async def on_ready():
   print('We have logged in as {0.user}'.format(client))
   
@client.event
async def on_message(message):
    if not message.content.startswith(PREFIX):
        return
    command = message.content[len(PREFIX):]

client.run(TOKEN)
