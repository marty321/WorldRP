import EconomyInterface as EI
import fileManagement as files
import disnake

PREFIX = ".."

def onMessage(message, client):
    args = message.content[len(PREFIX):].split(" ")
    command = args.pop(0)

    files.initialisePlayer(str(message.author.id),str(message.guild.id))
    
    if command == "leaderboard":
        return topTenFormat(str(message.guild.id),client)

def topTenFormat(serverID, client):
    topTenDict = EI.getTopTen(serverID)

    lbEmbed = disnake.Embed(
        title="Leaderboard",
        color=disnake.Colour.blue())

    for player in topTenDict:
        client.get_user(int(player))
        lbEmbed.add_field(
            name = str(client.get_user(player)),
            value = topTenDict[player],
            inline=False
            )

    return lbEmbed
