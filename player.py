import json
import pathlib
import requests
import matplotlib as mplot
from fmp_api import *


with open("dataBase.json", "r") as f:
    players = json.load(f)
    
# if __name__ == "__main__":
#     for player in players.items():
#         print(player)
#         print(end="\n")\

class Player():
    def __init__(self, discordID):
        self.disID = discordID
        values = {}
        values["balance"] = 100000
        values["portfolio"] = []
        values["cryptoWallet"] = []
        values["performance"] = []
        values["history"] = []

    def isPlaying(self):
        with open("dataBase.json", 'r+') as file:
            #load the data from the json file
            fileData = json.load(file)
            
            print(self.disID)
            print(fileData.keys())

            if self.disID in fileData.keys():
                print("Player will be added")
                return 0
            else:
                print(f"{self.disID} is a player already")
                return 1

    def writeJson(self, discordID, toBeAdded, fileName = 'dataBase.json'):
        with open(fileName, 'r+') as file:
            fileData = json.load(file)
            fileData[discordID] = toBeAdded
            file.seek(0)
            json.dump(fileData, file, indent = 4)

def buyStock(type, ticker):
    return get_price(ticker, type)


# new = Player(10003)            
# new.isPlaying()

print (type(buyStock("stock", "AAPL")))
# with open('dataBase.json', 'r+') as file:
#     #load the data from the json file
#     fileData = json.load(file)

#     name = "10003"

#     if name in fileData:
#         print(True)