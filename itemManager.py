import fileManagement as files
import disnake
import configManager as configs

'''
internalRole
role
cash
incomeRole
item
'''

def setDescription(itemName, serverID, description):
    item = files.getItem(itemName, serverID)
    item.description = ""
    for word in description:
        item.description += f" {word}"
    files.saveItem(item)

def setSingleBuy(itemName, serverID, isSingleBuy):
    if isSingleBuy == "false":
        isSingleBuy = False
    elif isSingleBuy == "true":
        isSingleBuy = True
        
    item = files.getItem(itemName, serverID)
    item.isSingleBuy = isSingleBuy
    files.saveItem(item)

def setRequirements(itemName, serverID, args):
    item = files.getItem(itemName, serverID)
    item.requirements = []
    for requirement in args:
        item.requirements.append(requirement)
    files.saveItem(item)
    
def onItemMessage(args,serverID):
    returnMessage,embed,file = None,None,None
    subcmd = args.pop(0)
    if subcmd == "create":
        newItemName = args[0]
        if newItemName not in files.getAllItems(serverID):
            newItem = files.Item(newItemName, serverID)
            files.saveItem(newItem)
        else:
            returnMessage = "item with that name already exists"
    elif subcmd == "description":
        setDescription(args.pop(0),serverID,args)

    elif subcmd == "singlebuy":
        setSingleBuy(args.pop(0),serverID,args[0])

    elif subcmd == "requirements":
        name = args.pop(0)
        setRequirements(name,serverID,args)

    elif subcmd == "get":
        item = files.getItem(args[0], serverID)
        embed = formatItem(item)
        

    return returnMessage,embed,file

def formatItem(item):
    embed = disnake.Embed(
            title = item.name,
            color=disnake.Colour.blue())
    if item.description:
        embed.add_field(
        name="Description:",
        value= item.description,
        inline=False
        )
        
    moreInfo = ""
    
    if item.requirements:
        moreInfo += "Requires: "
        for i in item.requirements:
            moreInfo += f"{i},"
        moreInfo = moreInfo[:-1]

    if item.rewards:
        moreInfo += "Rewards: "
        for i in item.rewards:
            moreInfo += f"{i},"
        moreInfo = moreInfo[:-1]

    moreInfo += f"\nCan buy once: {item.isSingleBuy}"

    moreInfo += f"\nConsumable: {item.isConsumable}"

    embed.add_field(
        name="Extra Info",
        value= moreInfo,
        inline=False
        )
        
    return embed

def buy(discordID,serverID,itemName,number,guild):
    returnMessage = None
    item = files.getItem(itemName,serverID)
    canBuy = True
    for requirement in item.requirements:
        if not checkRequirement(discordID, serverID, requirement, number, guild):
            canBuy = False

    if canBuy:
        returnMessage = "You succesfully bought this item"
        player = files.getPlayer(discordID, serverID)
        for requirement in item.requirements:
            removeCosts(discordID, serverID, requirement, player, number)
        try:
            player.inventory[item.name] += number
        except KeyError:
            player.inventory[item.name] = number
        files.savePlayer(player)
    else:
        returnMessage = "you dont meet criteria to buy this item"
    return returnMessage
    

def shop(serverID):
    embed = None
    allItems = files.getAllItems(serverID)
    embed = disnake.Embed(
            title = "Shop",
            color=disnake.Colour.blue())

    for itemName in allItems:
        item = files.getItem(itemName, serverID)

        requirements = ""
        if item.requirements:
            for i in item.requirements:
                if i.startswith("cash."):
                    print(i)
                    amount = i[len("cash."):]
                    symbol = configs.getConfig(serverID, "serverCurrencySymbol")
                    requirements += f"{amount} {symbol},"
            requirements = requirements[:-1]

        if not requirements:
            requirements = "free"
        embed.add_field(
            name=item.name,
            value=str(requirements),
            inline=False
            )

    return embed

def checkRequirement(discordID, serverID, requirement, number, guild):
    player = files.getPlayer(discordID, serverID)
    args = requirement.split(".")
    if args[0] == "cash":
        amount = int(args[1])
        return player.cash >= (amount * number)
    elif args[0] == "role":
        for role in guild.roles:
            if role.id == int(args[1]):
                for member in role.members:
                    if member.id == int(discordID):
                        print(member.id)
                        return True
        return False
    elif args[0] == "internalRole":
        return args[1] in player.roles
    elif args[0] == "incomeRole":
        return args[1] in player.incomeTechs
    elif args[0] == "item":
        return args[1] in player.inventory

def removeCosts(discordID, serverID, requirement, player, number):
    args = requirement.split(".")
    if args[0] == "cash":
        player.cash -= int(args[1]) * number
    
