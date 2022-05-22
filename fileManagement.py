import os

def add_server(guild_id):
    serversDir = ".\\servers"
  
    currentServers = [f.path for f in os.scandir(".") if f.is_dir()]
    if serversDir not in currentServers:
        os.mkdir(serversDir)

    try:
        directory = str(guild_id)
        path = os.path.join(serversDir, directory)
        os.mkdir(path)
    except FileExistsError:
        pass
