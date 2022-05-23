import json
from fmp_api import Query

def readJson(file='database.json'):
    with open(file) as database:
        return json.load(database)

def writeJson(data, file='database.json'):
    with open(file, "w") as database:
        json.dump(data, database, indent = 4)
    database.close()

def appendJson(user_id, user_dict, file='database.json'):
    full_data = readJson()
    full_data[user_id] = user_dict
    writeJson(full_data)

def make_leaderboard():
    data = readJson()
    leader_board = []

    

class Player():
    def __init__(self, user: str):
        self.user = user
        data = readJson()
        if self.user in data:
            self.profile = data[user]
        else:
            self.profile = {}
            self.profile['cash'] = 100000
            self.profile['portfolio'] = {}
            appendJson(self.user, self.profile)

    def buy_asset(self, query: Query, quantity):
        value = query.price * quantity

        if self.profile['cash'] < value:
            status = 'nsf'
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
                self.profile['cash'] += value
                status = True
        else:
            print("Portfolio does not contain this asset")
            status = 'nsa'

        appendJson(self.user, self.profile)
        return status

    def get_networth(self):
        net_worth = self.profile['cash']
        if len(self.profile['portfolio']) <= 0:
            return net_worth
        else:
            for key, value in self.profile['portfolio'].items():
                query = Query(key)
                net_worth += (query.price * value)
            return net_worth
    



# userID = input("Input the user ID: ")

# newPlayer = Player(userID)
# #data[userID]['portfolio']['AAPL'] = 10


# # record = {}
# # record["APPLE"] = 20
# # data[userID]['portfolio'] = record

# # record["TSLA"] = 30
# # data[userID]['portfolio'] = record

# # print(data[userID]['portfolio'])
# newPlayer.buy_asset("TSLA", 10)
# # newPlayer.sell_asset("TSLA", 40)

# print(newPlayer.get_networth())

# print(newPlayer)