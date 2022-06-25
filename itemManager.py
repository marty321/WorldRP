import files
import disnake

class Item:
    def __init__(self, name, serverID, description=None, requirements=[], isSingleBuy=False, rewards=[], isConsumable=True):
        self.name = name
        self.description = description
        self.requirements = requirements
        self.isSingleBuy = isSingleBuy
        self.rewards = rewards
        self.isConsumable = isConsumable
        self.serverID = serverID

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

def onItemMessage(args,serverID):
    returnMessage,embed,file = None,None,None
    subcmd = args.pop(0)
    if subcmd == "create":
        newItemName = args[0]
        if newItemName not in getAllItems(serverID):
            newItem = Item(newItemName, serverID)
            saveItem(newItem)
        else:
            returnMessage = "item with that name already exists"
    elif subcmd == "description":
        setDescription(args.pop(0),serverID,args)

    elif subcmd == "singlebuy":
        setSingleBuy(args.pop(0),serverID,args[0])

    elif subcmd == "get":
        item = getItem(args[0], serverID)
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
        
    moreInfo = "*"
    
    if item.requirements:
        moreInfo += "Requires:"
        for i in item.requirements:
            moreInfo += f"{i},"
        moreInfo = moreInfo[:-1]

    if item.rewards:
        moreInfo += "Rewards:"
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
    moreInfo += "*"
        
    return embed
