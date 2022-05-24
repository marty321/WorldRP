import fileManagement as files
import botUtils
import operator
import collections

def addMoney(discordID,serverID,amount):
    player = files.getPlayer(discordID,serverID)
    player.cash += amount
    savePlayer(player)

def minusMoney(discordID,serverID,amount):
    player = files.getPlayer(discordID,serverID)
    player.cash -= amount
    savePlayer(player)

def addInv(discordID,serverID,item, amount):
    player = files.getPlayer(discordID,serverID)
    try:
        player.inventory[item] += amount
    except KeyError:
        player.inventory[item] = amount
    savePlayer(player)

def removeInv(discordID,serverID,item, amount):
    player = files.getPlayer(discordID,serverID)
    player.inventory[item] -= amount
    savePlayer(player)

def getInvAmount(discordID,serverID,item):
    try:
        player = files.getPlayer(discordID,serverID)
    except KeyError:
        return 0
    return player.inventory[item]

def getCashAmount(discordId,serverID):
    player = files.getPlayer(discordID,serverID)
    return player.cash

def getIncomeTechs(discordId,serverID):
    player = files.getPlayer(discordID,serverID)
    return player.incomeTechs

def getTopTen(serverID):
    allPlayers = files.getAllPlayers(serverID)
    topTen = {}
    minCash = 0
    for player in allPlayers:
        player = files.getPlayer(player, serverID)
        if player.cash > minCash:
            topTen[player.discordID] = player.cash
    
    sortedTopTen = sorted(topTen.items(),key=operator.itemgetter(1))
    sortedTopTenDict = dict(collections.OrderedDict(sortedTopTen))
    
    return sortedTopTenDict

