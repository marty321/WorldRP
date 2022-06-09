def getDiscordID(discordID):
    if discordID.isdigit():
        return discordID
    elif discordID.endswith(">") and discordID.startswith("<@"):
        return discordID[2:-1]
