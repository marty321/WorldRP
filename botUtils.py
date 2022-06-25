import EconomyInterface as EI
import fileManagement as files
import disnake
import discordUtils as DU
import configManager as configs
import itemManager as items


def onMessage(message, client):
    blacklisted = configs.getConfig(str(message.guild.id), "blacklist")
    whitelisted = configs.getConfig(str(message.guild.id), "whitelist")
    
    prefix = configs.getConfig(str(message.guild.id),"serverPrefix")
    selfPing = DU.pingUser(str(client.user.id))
    messageContent = message.content.strip()
    if messageContent.startswith(selfPing):
        prefix = selfPing
        
    elif not messageContent.startswith(prefix):
        return None,None,None
    elif whitelisted:
        if str(message.channel.id) not in whitelisted:
            return None,None,None
    elif str(message.channel.id) in blacklisted:
        return None,None,None
    
    args = message.content[len(prefix):].lower()
    args = args.split(" ")
    while "" in args:
        args.remove("")
    command = args.pop(0).lower()

    returnMessage,embed,file = None,None,None
    
    files.initialisePlayer(str(message.author.id),str(message.guild.id))

    serverID = str(message.guild.id)
    
    if command == "leaderboard":
        embed = topTenFormat(serverID,client)

    elif command == "player":
        discordID = str(message.author.id)
        if args:
            discordID = DU.getDiscordID(args[0])
        embed = playerFormat(discordID,serverID, client)

    elif command == "prefix":
        prefix = configs.getConfig(serverID,"serverPrefix")
        returnMessage = f"prefix is {prefix}"

    elif command == "collect":
        discordID = str(message.author.id)
        serverID = str(message.guild.id)
        returnMessage,embed,file = EI.collect(serverID, discordID)
        
    elif not DU.checkPermissions(message.author, serverID):
        pass
    
    elif command == "addinventory":
        discordID = DU.getDiscordID(args[0])
        EI.addInv(discordID,serverID,args[1],args[2])

    elif command == "removeinventory":
        discordID = DU.getDiscordID(args[0])
        EI.removeInv(discordID,serverID,args[1],args[2])

    elif command == "addmoney":
        discordID = DU.getDiscordID(args[0])
        EI.addMoney(discordID,serverID,args[1])

    elif command == "removemoney":
        discordID = DU.getDiscordID(args[0])
        EI.minusMoney(discordID,serverID,args[1])

    elif command == "removeincomerole":
        discordID = DU.getDiscordID(args[0])
        EI.removeIncome(discordID,serverID,args[1])

    elif command == "resetplayer":
        discordID = DU.getDiscordID(args[0])
        files.deletePlayer(discordID,serverID)
        files.initialisePlayer(discordID,serverID)

    elif command == "setincomerole":
        name = args.pop(0)
        amount = args.pop(0)
        time = args.pop(0)
        files.setIncomeRole(serverID,name,amount,time)

    elif command == "giveincomerole":
        name = args[1]
        if args[0] == "all":
            discordID = args[0]
        else:
            discordID = DU.getDiscordID(args[0])
        files.giveIncomeRoles(name,discordID,serverID)

    elif command == "item":
        returnMessage,embed,file = items.onItemMessage(args,serverID)
        
    elif command == "config":
        returnMessage,embed,file = configs.onMessage(args, str(message.guild.id))

    return returnMessage,embed,file

def topTenFormat(serverID, client):
    topTen = EI.getTopTen(serverID)

    cashSymbol = configs.getConfig(serverID, "serverCurrencySymbol")

    lbEmbed = disnake.Embed(
        title="Leaderboard",
        color=disnake.Colour.blue())

    place = 1
    
    for player in topTen:
        user = f"{place}) {client.get_user(int(player[0]))}"
        lbEmbed.add_field(
            name = user,
            value = f"{player[1]} {cashSymbol}",
            inline=False
            )
        place += 1

    return lbEmbed

def playerFormat(discordID, serverID, client):
    player = files.getPlayer(discordID,serverID)
    cashSymbol = configs.getConfig(serverID, "serverCurrencySymbol")
    
    playerEmbed = disnake.Embed(
        title = client.get_user(int(discordID)).name,
        color=disnake.Colour.blue())

    playerEmbed.add_field(
        name="Cash",
        value=f"{player.cash} {cashSymbol}",
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
    
