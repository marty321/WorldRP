import fileManagement as files

def getDiscordID(discordID):
    if discordID.isdigit():
        return discordID
    elif discordID.endswith(">") and discordID.startswith("<@"):
        discordID = discordID[2:-1]
        if discordID.startswith("&"):
            return discordID[1:]
        return discordID
    elif discordID.endswith(">") and discordID.startswith("<#"):
        return discordID[2:-1]

def checkPermissions(discordUser, serverID):
    if discordUser.guild_permissions.administrator:
        return True

    allPerms = files.getPerms(serverID)
    if str(discordUser.id) in allPerms:
        return True
    
    for role in discordUser.roles:
        if str(role.id) in allPerms:
            return True
    return False

def pingUser(discordID):
    return f"<@{discordID}>"

def pingChannel(discordID):
    return f"<#{discordID}>"
