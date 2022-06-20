import os
import pickle
import time
import re

SERVERS_DIR = ".\\servers"
FILES = {"config": "config.txt",
         "perms": "perms.txt",
         "income": "incomeRoles.txt"}

class Player:
    def __init__(self,_discordID,_serverID,_cash = 5,_incomeTechs = {},_inventory = {}):
        self.discordID = _discordID
        self.serverID = _serverID
        self.cash = _cash
        self.incomeTechs = _incomeTechs
        self.inventory = _inventory
        

def add_server(guild_id):
    currentServers = [f.path for f in os.scandir(".") if f.is_dir()]
    if SERVERS_DIR not in currentServers:
        os.mkdir(SERVERS_DIR)

    try:
        directory = str(guild_id)
        path = os.path.join(SERVERS_DIR, directory)
        os.mkdir(path)
        for file in FILES.values():
            newPath = path + f"\\{file}"
            createFile = open(newPath,"w")
            createFile.close()
            
    except FileExistsError:
        pass

def deletePlayer(discordID,serverID):
    serverPath = os.path.join(SERVERS_DIR,serverID)
    userPath = os.path.join(serverPath,discordID)
    os.remove(userPath)
    
def initialisePlayer(discordID, ServerID):
    newPlayer = Player(discordID, ServerID)
    serverPath = os.path.join(SERVERS_DIR,ServerID)
    userPath = os.path.join(serverPath,discordID)
    try:
        testOpen = open(userPath,"r")
        testOpen.close()
    except FileNotFoundError:
        userFile = open(userPath,"wb")
        pickle.dump(newPlayer, userFile)
        userFile.close()

def getPlayer(discordID, serverID):
    serverPath = os.path.join(SERVERS_DIR,serverID)
    userPath = os.path.join(serverPath,discordID)
    try:
        userFile = open(userPath,"rb")
        user = pickle.load(userFile)
        userFile.close()
    except FileNotFoundError:
        initialisePlayer(discordID, serverID)
        user = getPlayer(discordID, serverID)
    return user

def savePlayer(user):
    serverPath = os.path.join(SERVERS_DIR,user.serverID)
    userPath = os.path.join(serverPath,user.discordID)
    userFile = open(userPath,"wb")
    pickle.dump(user, userFile)
    userFile.close()

def getAllPlayers(serverID):
    serverPath = os.path.join(SERVERS_DIR,serverID)
    fileList = [f for f in os.listdir(serverPath) if os.path.isfile(os.path.join(serverPath, f)) and f not in FILES]
    for file in FILES.values():
        fileList.remove(file)
    return fileList

def addPerms(discordID,serverID):
    serverPath = os.path.join(SERVERS_DIR,serverID)
    permPath = os.path.join(serverPath,FILES["perms"])
    with open(permPath,"a") as permFile:
        permFile.write(discordID + "\n")

def remPerms(discordID,serverID):
    serverPath = os.path.join(SERVERS_DIR,serverID)
    permPath = os.path.join(serverPath,FILES["perms"])
    permContent = getPerms(serverID)
    with open(permPath,"w+") as permFile:
        for user in permContent:
            if discordID != user.strip():
                permFile.write(user)

def getPerms(serverID):
    serverPath = os.path.join(SERVERS_DIR,serverID)
    permPath = os.path.join(serverPath,FILES["perms"])
    totalPerms = []
    with open(permPath,"r") as permFile:
        for line in permFile:
            totalPerms.append(line[:-1])
    return totalPerms

def setIncomeRole(serverID,name,amount,time):
    serverPath = os.path.join(SERVERS_DIR,serverID)
    incomePath = os.path.join(serverPath,FILES["income"])
    with open(incomePath, "a") as incomeFile:
        unit = time[-1]
        time = int(time[:-1])
        if unit == "d":
            time *= 24
            unit = "h"
        if unit == "h":
            time *= 60
            unti = "m"
        if unit == "m":
            time *= 60
            unit = "s"
        
        line = f"{name},{str(amount)},{time}"
        incomeFile.write(line)

def getIncomeRoles(serverID):
    serverPath = os.path.join(SERVERS_DIR,serverID)
    incomePath = os.path.join(serverPath,FILES["income"])
    incomeRoles = {}
    with open(incomePath, "r") as incomeFile:
        for line in incomeFile:
            splitAmount = re.split("[]",line)
            name = splitAmount[0]
            

    

