import json
from fmp_api import Query


def readJson(file='database.json'):
    with open(file) as database:
        return json.load(database)


def writeJson(data, file='database.json'):
    with open(file, "w") as database:
        json.dump(data, database, indent = 4)
    database.close()


def appendJson(user_id, user_dict):
    full_data = readJson()
    full_data[user_id] = user_dict
    writeJson(full_data)


def make_leaderboard():
    data = readJson()
    leader_board = []
    for player_index, profile_index in data.items():
        leader_board.append([profile_index['discord_name'], float(profile_index['net_worth'])])

    
    for i in range(len(leader_board) - 1):
        for j in range(len(leader_board) - i - 1):
            if leader_board[j][1] > leader_board[j + 1][1]:
                leader_board[j], leader_board[j + 1] = leader_board[j + 1], leader_board[j]
        
    return leader_board[::-1]


class Player():

    def __init__(self, user, discord_name):
        self.user = user
        data = readJson()
        if self.user in data:
            self.profile = data[user]
            self.profile['net_worth'] = self.get_net_worth()
        else:
            self.profile = {}
            self.profile['cash'] = 100000
            self.profile['portfolio'] = {}
            self.profile['net_worth'] = self.get_net_worth()
            self.profile['discord_name'] = discord_name
            appendJson(self.user, self.profile)


    def buy_asset(self, query: Query, quantity):
        value = query.price * quantity

        if self.profile['cash'] < value:
            status = 'nsf'
        else:
            if query.exchange == "CRYPTO":
                self.profile['cash'] -= value + (value * 0.015)
            else:
                self.profile['cash'] -= value
            
            if query.symbol in self.profile['portfolio']:
                self.profile['portfolio'][query.symbol] += quantity
                status = True
            else:
                self.profile['portfolio'][query.symbol] = quantity
                status = True
        appendJson(self.user, self.profile)
        return status


    def sell_asset(self, query: Query, quantity):
        value = query.price * quantity

        if query.symbol in self.profile['portfolio']:
            if quantity > self.profile['portfolio'][query.symbol]:
                print("Portfolio does not contain sufficient quantity of this asset")
                status = 'nsa'
            else:
                self.profile['portfolio'][query.symbol] -= quantity
                if query.exchange == "CRYPTO":
                    self.profile['cash'] += value - (value * 0.015)
                else:
                    self.profile['cash'] += value
                
                status = True
        else:
            print("Portfolio does not contain this asset")
            status = 'nsa'

        appendJson(self.user, self.profile)
        return status


    def get_net_worth(self):
        net_worth = self.profile['cash']
        if len(self.profile['portfolio']) <= 0:
            return net_worth
        else:
            for key, value in self.profile['portfolio'].items():
                query = Query(key)
                net_worth += (query.price * value)
            return net_worth
