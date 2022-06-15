import discordUtils as DU
import fileManagement as files
import pickle
import os

def onMessage(args, serverID):
    subCommand = args.pop(0).lower()
    returnMessage,embed,file = None, None, None

    if subCommand == "addpermissions":
        discordID = DU.getDiscordID(args[0])
        files.addPerms(discordID,serverID)

    elif subCommand == "removepermissions":
        discordID = DU.getDiscordID(args[0])
        files.remPerms(discordID,serverID)

    elif subCommand == "setcurrency":
        setConfig(serverID,"serverCurrencySymbol",args[0])
        returnMessage = f"server currency symbol set to {args[0]}"

    elif subCommand == "setprefix":
        setConfig(serverID,"serverPrefix",args[0])
        returnMessage = f"server prefix set to {args[0]}"

    elif subCommand in ["blacklist","whitelist"]:
        pre = ""
        if args[0] == "add":
            discordID = DU.getDiscordID(args[1])
            addConfig(serverID,subCommand,discordID)
        elif args[0] == "remove":
            discordID = DU.getDiscordID(args[1])
            removeConfig(serverID,subCommand,discordID)
            pre = "un"

        returnMessage = f"{pre}{subCommand}ed {args[1]}"
        
    return returnMessage,embed,file

def getConfigs(serverID):
    serverPath = os.path.join(files.SERVERS_DIR,serverID)
    configPath = os.path.join(serverPath,files.FILES["config"])
    configs = {}
    with open(configPath,"r",encoding="utf-16") as configFile:
        for line in configFile:
            line = line.strip()
            lineSplit = line.split(",")

            config = lineSplit.pop(0)
            configs[config] = lineSplit
            if len(lineSplit) == 1:
                configs[config] = lineSplit[0]
            
    return configs

def saveConfigs(serverID, configs):
    serverPath = os.path.join(files.SERVERS_DIR,serverID)
    configPath = os.path.join(serverPath,files.FILES["config"])
    with open(configPath,"w",encoding="utf-16") as configFile:
        for config in configs:
            values = configs[config]
            if type(values) == list:
                line = config
                for value in values:
                    line += "," + value
            else:
                line = f"{config},{configs[config]}\n"
            configFile.write(line)

def setConfig(serverID, config, value):
    configs = getConfigs(serverID)
    configs[config] = value
    saveConfigs(serverID, configs)

def getConfig(serverID ,config):
    configs = getConfigs(serverID)
    try:
        if len (configs[config]) == 1:
            return configs[config][0]
    except KeyError:
        return []
    return configs[config]

def addConfig(serverID ,config, value):
    configs = getConfigs(serverID)
    try:
        configs[config] = [configs[config]] + [value]
    except KeyError:
        configs[config] = value
    saveConfigs(serverID, configs)

def removeConfig(serverID ,config, value):
    configs = getConfigs(serverID)
    try:
        configs[config].remove(value)
    except AttributeError:
        configs[config] = ""
    saveConfigs(serverID, configs)



            

