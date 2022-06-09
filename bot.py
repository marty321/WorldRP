import disnake
import os
import fileManagement as files
import EconomyInterface as EI
import botUtils

intents = disnake.Intents.all()
client = disnake.Client(intents=intents)

tokenFile = open("token.txt","r")
TOKEN = tokenFile.read()
tokenFile.close()
if TOKEN == "":
  f = open("token.txt","w")
  f.close()
  raise RuntimeError("No token in token.txt")


@client.event
async def on_ready():
   print(f"We have logged in as {client.user}")
   for guild in client.guilds:
        print(f"{guild.name} (id:{str(guild.id)})")
        files.add_server(guild.id)
        

@client.event
async def on_guild_join(guild):
  files.add_server(guild.id)

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  try:
    returnMessage,embed,file = botUtils.onMessage(message,client)
  except RuntimeError as e:
    returnMessage = e
    
  await message.channel.send(returnMessage,embed=embed,file=file)

client.run(TOKEN)
