import fileManagement as files
import botUtils
import operator
import collections

def addMoney(discordID,serverID,amount):
    player = files.getPlayer(discordID,serverID)
    player.cash += int(amount)
    files.savePlayer(player)

def minusMoney(discordID,serverID,amount):
    player = files.getPlayer(discordID,serverID)
    player.cash -= int(amount)
    files.savePlayer(player)

def addInv(discordID,serverID,item, amount):
    player = files.getPlayer(discordID,serverID)
    try:
        player.inventory[item] += int(amount)
    except KeyError:
        player.inventory[item] = int(amount)
    files.savePlayer(player)

def removeInv(discordID,serverID,item, amount):
    player = files.getPlayer(discordID,serverID)
    player.inventory[item] -= int(amount)
    files.savePlayer(player)

def getInvAmount(discordID,serverID,item):
    try:
        player = files.getPlayer(discordID,serverID)
    except KeyError:
        return 0
    return player.inventory[item]

def addIncome(discordID,serverID,income):
    player = files.getPlayer(discordID,serverID)
    player.incomeTechs.append(income)
    files.savePlayer(player)

def removeIncome(discordID, serverID, income):
    player = files.getPlayer(discordID,serverID)
    player.incomeTechs.remove(income)
    files.savePlayer(player)

def getCashAmount(discordId,serverID):
    player = files.getPlayer(discordID,serverID)
    return player.cash

def getIncomeTechs(discordId,serverID):
    player = files.getPlayer(discordID,serverID)
    return player.incomeTechs

def getTopTen(serverID):
    allPlayers = files.getAllPlayers(serverID)
    allUsers = {}
    for player in allPlayers:
        player = files.getPlayer(player,serverID)
        try:
            allUsers[player.cash].append(player.discordID)
        except KeyError:
            allUsers[player.cash] = [player.discordID]

    moneyAmounts = list(allUsers.keys())
    moneyAmounts.sort(reverse=True)
    topTen = []
    for amount in moneyAmounts:
        for player in allUsers[amount]:
            topTen.append((player, amount))
        if len(topTen) >= 10:
            break

    print(topTen)
        
    return topTen

