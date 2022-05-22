import json
import pathlib
import requests
import matplotlib as mplot


with open("config.json", "r") as f:
    players = json.load(f)
    
    
if __name__ == "__main__":
    for player in players:
        print(type(player))