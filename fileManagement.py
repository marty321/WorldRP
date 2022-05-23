import os
import pickle

SERVERS_DIR = ".\\servers"

class Player:
    def __init__(self,_discordID,_cash = 5,_incomeTechs = [],_inventory = {}):
        self.discordID = _discordID
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
    except FileExistsError:
        pass

def initialisePlayer(discordID, ServerID):
    newPlayer = Player(discordID)
    serverPath = os.path.join(SERVERS_DIR,ServerID)
    userPath = os.path.join(serverPath,discordID)
    try:
        testOpen = open(userPath,"r")
        testOpen.close()
    except FileNotFoundError:
        userFile = open(userPath,"wb")
        pickle.dump(newPlayer, userFile)
        userFile.close()

def getPlayer(discordID, ServerID):
    serverPath = os.path.join(SERVERS_DIR,ServerID)
    userPath = os.path.join(serverPath,discordID)
    try:
        userFile = open(userPath,"rb")
        user = pickle.load(userFile)
        userFile.close()
    except FileNotFoundError:
        initialisePlayer(discordID, ServerID)
        user = getPlayer(discordID, ServerID)
    return user
    

