import EconomyInterface as EI
import fileManagement as files
import disnake

PREFIX = ".."

def onMessage(message, client):
    args = message.content[len(PREFIX):].split(" ")
    while "" in args:
        args.remove("")
    command = args.pop(0)

    returnMessage,embed,file = None,None,None
    
    files.initialisePlayer(str(message.author.id),str(message.guild.id))
    
    if command == "leaderboard":
        embed = topTenFormat(str(message.guild.id),client)

    elif command == "player":
        embed = embedFormat(args[0], str(message.guild.id), client)

    elif command == "addinventory":
        if args[0].endswith(">") and args[0].startswith("<@"):
            discordID = args[0][2:-1]
            EI.addInv(discordID,str(message.guild.id),args[1],args[2])

    elif command == "removeinventory":
        if args[0].endswith(">") and args[0].startswith("<@"):
            discordID = args[0][2:-1]
            print(args)
            EI.removeInv(discordID,str(message.guild.id),args[1],args[2])

    return returnMessage,embed,file

def topTenFormat(serverID, client):
    topTenDict = EI.getTopTen(serverID)

    lbEmbed = disnake.Embed(
        title="Leaderboard",
        color=disnake.Colour.blue())

    place = 1
    
    for player in topTenDict:
        user = f"{place}) {client.get_user(int(player))}"
        lbEmbed.add_field(
            name = user,
            value = topTenDict[player],
            inline=False
            )
        place += 1

    return lbEmbed

def embedFormat(discordID, serverID, client):
    if not(discordID.endswith(">") and discordID.startswith("<@")):
        return
    discordID = discordID[2:-1]
    
    player = files.getPlayer(discordID,serverID)
    playerEmbed = disnake.Embed(
        title = client.get_user(int(discordID)).name,
        color=disnake.Colour.blue())

    playerEmbed.add_field(
        name="Cash",
        value=player.cash,
        inline=False
        )

    techString = ""
    for income in player.incomeTechs:
        techString += ",",income
    if techString == "":
        techString = "None"
    playerEmbed.add_field(
        name="Income Techs",
        value=techString,
        inline=False
        )

    invString = ""
    for invItem in player.inventory.keys():
        invString += invItem + " × " + str(player.inventory[invItem]) + "\n"
    if invString == "":
        invString = "None"
    playerEmbed.add_field(
        name="Inventory",
        value=invString,
        inline=False
        )

    return playerEmbed
    
