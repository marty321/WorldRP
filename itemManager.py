import fileManagement as files
import disnake
import configManager as configs
import discordUtils as DU

    
def onItemMessage(args,guild):
    serverID = str(guild.id)
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
        embed = formatItem(item, guild)

    elif subcmd == "rewards":
        name = args.pop(0)
        setRewards(name,serverID,args)

    else:
        returnMessage="unknown command"
        
    return returnMessage,embed,file

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
        args = requirement.split(".")
        if args[0] == "role":
            roleID = DU.getDiscordID(args[1])
            requirement = f"role.{roleID}"
        item.requirements.append(requirement)
    files.saveItem(item)


def setRewards(itemName, serverID, args):
    item = files.getItem(itemName, serverID)
    item.rewards = []
    for requirement in args:
        args = requirement.split(".")
        if args[0] == "role":
            roleID = DU.getDiscordID(args[1])
            requirement = f"role.{roleID}"
        item.rewards.append(requirement)
    files.saveItem(item)


def formatItem(item, guild):
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
            args = i.split(".")
            if args[0] == "role":
                i = f"role.{guild.get_role(int(args[1]))}"
            moreInfo += f"'{i}',"
        moreInfo = moreInfo[:-1]

    if item.rewards:
        moreInfo += "\nRewards: "
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
    errors = ""
    for requirement in item.requirements:
        passed,error = checkRequirement(discordID, serverID, requirement, number, guild)
        if error:
            errors += f"{error}\n"
        if not passed:
            canBuy = False

    if canBuy:
        returnMessage = "You succesfully bought this item"
        player = files.getPlayer(discordID, serverID)
        for requirement in item.requirements:
            removeCosts(requirement, player, number)
        try:
            player.inventory[item.name] += number
        except KeyError:
            player.inventory[item.name] = number
        files.savePlayer(player)
    else:
        returnMessage = f"you dont meet criteria to buy this item\nMore info:\n{errors}"
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
    error = ""
    if args[0] == "cash":
        amount = int(args[1])
        passed = player.cash >= (amount * number)
        if not passed:
            error = "not enough money"
        return passed,error
    elif args[0] == "role":
        for role in guild.roles:
            if role.id == int(args[1]):
                for member in role.members:
                    if member.id == int(discordID):
                    
                        return True,error
        error = "missing required role"
        return False,error
    elif args[0] == "internalrole":
        passed = args[1] in player.roles
        if passed:
            error = "missing require internal role"
        return passed,error
    elif args[0] == "incomerole":
        passed = args[1] in player.incomeTechs
        if not passed:
            error = "missing required income role"
        return passed,error
    elif args[0] == "item":
        passed = args[1] in player.inventory
        if not passed:
            error = "missing required item"
        return passed,error
    else:
        return False,"an error has occured"

def removeCosts(requirement, player, number):
    args = requirement.split(".")
    if args[0] == "cash":
        player.cash -= int(args[1]) * number

def use(discordID, serverID, itemName, number, guild):
    item = files.getItem(itemName,serverID)
    player = files.getPlayer(discordID, serverID)
    returnMessage = None
    try:
        if player.inventory[itemName] < number:
            return "you don't own enough of this item"
    except KeyError:
        return "you do not own this item"

    for i in range(number):
            player.inventory[itemName] -= 1
            
    for reward in item.rewards:
        giveRewards(reward,player,number)
    files.savePlayer(player)

    return returnMessage

def giveRewards(reward, player, number):
    args = reward.split(".")
    if args[0] == "cash":
        player.cash += int(args[1]) * number
    elif args[0] == "internalrole":
        player.roles.append(args[1])
    elif args[0] == "role":
        pass
    elif args[0] == "incomerole":
        player.incomeTechs[args[1]] = 0
    elif args[0] == "item":
        for counter in range(number):
            player.inventory.append(args[1])
        
    
