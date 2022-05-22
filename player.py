import json
import pathlib
import requests
import matplotlib as mplot


with open("dataBase.json", "r") as f:
    players = json.load(f)
    
# if __name__ == "__main__":
#     for player in players.items():
#         print(player)
#         print(end="\n")\

class Player():
    def __init__(self, discordID):
        def isPlaying(discordID):
            with open("dataBase.json", 'r+') as file:
                #load the data from the json file
                fileData = json.load(file)
                print(fileData.keys())
                if fileData.get(discordID) is None:
                    return 0
                else:
                    print(discordID, "is already playing")
                    return 1

        def writeJson(discordID, toBeAdded, fileName = 'dataBase.json'):
            with open(fileName, 'r+') as file:
                fileData = json.load(file)
                fileData[discordID] = toBeAdded
                file.seek(0)
                json.dump(fileData, file, indent = 4)

        if isPlaying(discordID) == 0:
            values = {}
            values["balance"] = 100000
            values["portfolio"] = []
            values["cryptoWallet"] = []
            values["performance"] = []
            values["history"] = []
            writeJson(discordID, values)
            
new = Player(10003)
new1 = Player(10003)

# with open('dataBase.json', 'r+') as file:
#     #load the data from the json file
#     fileData = json.load(file)

#     name = "10003"

#     if name in fileData:
#         print(True)