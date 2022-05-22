import disnake
import os
import fileManagement as files

intents = disnake.Intents.all()
client = disnake.Client(intents=intents)

PREFIX = ".."

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


client.run(TOKEN)
