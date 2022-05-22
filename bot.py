import disnake
import os

client = disnake.Client()

PREFIX = ".."

tokenFile = open("token.txt","r")
TOKEN = tokenFile.read()
tokenFile.close()
print(TOKEN)
if TOKEN == "":
  f = open("token.txt","w")
  f.close()
  raise RuntimeError("No token in token.txt")


@client.event
async def on_ready():
   print('We have logged in as {0.user}'.format(client))


client.run(TOKEN)
