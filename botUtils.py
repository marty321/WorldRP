import EconomyInterface as EI
import fileManagement as files
import disnake
import discordUtils as DU

PREFIX = ".."

def onMessage(message, client):
    args = message.content[len(PREFIX):].split(" ")
    while "" in args:
        args.remove("")
    command = args.pop(0).lower()

    returnMessage,embed,file = None,None,None
    
    files.initialisePlayer(str(message.author.id),str(message.guild.id))
    
    if command == "leaderboard":
        embed = topTenFormat(str(message.guild.id),client)

    elif command == "player":
        discordID = DU.getDiscordID(args[0])
        embed = playerFormat(discordID, str(message.guild.id), client)

    elif command == "addinventory":
        discordID = DU.getDiscordID(args[0])
        EI.addInv(discordID,str(message.guild.id),args[1],args[2])

    elif command == "removeinventory":
        discordID = DU.getDiscordID(args[0])
        EI.removeInv(discordID,str(message.guild.id),args[1],args[2])

    elif command == "addmoney":
        discordID = DU.getDiscordID(args[0])
        EI.addMoney(discordID,str(message.guild.id),args[1])

    elif command == "removemoney":
        discordID = DU.getDiscordID(args[0])
        EI.minusMoney(discordID,str(message.guild.id),args[1])

    elif command == "addincome":
        discordID = DU.getDiscordID(args[0])
        EI.addIncome(discordID,str(message.guild.id),args[1])

    elif command == "removeincome":
        discordID = DU.getDiscordID(args[0])
        EI.removeIncome(discordID,str(message.guild.id),args[1])

    elif command == "config":
        pass

    return returnMessage,embed,file

def topTenFormat(serverID, client):
    topTen = EI.getTopTen(serverID)

    lbEmbed = disnake.Embed(
        title="Leaderboard",
        color=disnake.Colour.blue())

    place = 1
    
    for player in topTen:
        user = f"{place}) {client.get_user(int(player[0]))}"
        lbEmbed.add_field(
            name = user,
            value = player[1],
            inline=False
            )
        place += 1

    return lbEmbed

def playerFormat(discordID, serverID, client):
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
        techString += income + ", "
    techString = techString[:-2]
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
    
