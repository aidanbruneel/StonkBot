from urllib.request import urlopen
import certifi
import json
import math

from  data_plotting import plot # might not need this
import settings

class Query:
    def __init__(self, symbol: str, includeData: bool = False):
        self.__symbol = symbol
        # Quote
        self.__quote = self.get_quote()
        self.__profile = self.get_profile()
        #self.__history = self.get_history("15min")

    def web_scrape(self, url: str): # Returns dict
        data = urlopen(url, cafile=certifi.where()).read().decode('utf-8')

        if json.loads(data): # if symbol was found
            return json.loads(data)[0]
        else:
            return None

    def get_quote(self):
        url = (f"https://financialmodelingprep.com/api/v3/quote/{self.__symbol}?apikey={settings.API_KEY}")
        return self.web_scrape(url)

    # def get_history(self, interval: str):
    #     url = (f"https://financialmodelingprep.com/api/v3/historical_chart/{interval}/{self.__symbol}?apikey={settings.API_KEY}")
        
    #     data = urlopen(url, cafile=certifi.where()).read().decode('utf-8')

    #     if json.loads(data):
    #         data = json.loads(data)
    #         x = [math.average(time_info['open'], time_info['closed']) for time_info in data][::-1]
    #         return x
    #     else:
    #         return None
    
    def get_profile(self):
        url = (f"https://financialmodelingprep.com/api/v3/profile/{self.__symbol}?apikey={settings.API_KEY}")
        return self.web_scrape(url)
    
    @property
    def quote(self):
        return self.__quote
    
    @property
    def image(self):
        return self.__profile['image']
    
    @property
    def website(self):
        match (self.__profile is not None):
            case True:
                return self.__profile['website']
            case False:
                return None
    
    # @property
    # def open_history(self,interval:str):
    #     return self.__history
    
    #sum_list = [a + b for a, b in zip(list1, list2)]
    #divide values in new list by 2 - these will be the y-values for the plot
    
    @property
    def name(self):
        return self.__quote['name']

    @property
    def description(self):
        return self.__profile['description']
        
    @property
    def exchange(self):
        return self.__quote['exchange']
    
    @property
    def price(self):
        return self.__quote['price']

    @property
    def price_change(self):
        return self.__quote['change']
    
    @property
    def market_cap(self):
        return self.__quote['marketCap']
    
    @property
    def pe_ratio(self):
        return self.__quote['pe']
    
    @property
    def change(self):
        return self.__quote['change']
 
    @property
    def change_percent(self):
        return self.__quote['changesPercentage']

    @property
    def day_low(self):
        return self.__quote['dayLow']

    @property
    def day_high(self):
        return self.__quote['dayHigh']

    @property
    def year_high(self):
        return self.__quote['yearHigh']

    @property
    def year_low(self):
        return self.__quote['yearLow']

    @property
    def price_avg_50d(self):
        return self.__quote['priceAvg50']

    @property
    def price_avg_200d(self):
        return self.__quote['priceAvg200']
        
    @property
    def volume(self):
        return self.__quote['volume']

    @property
    def avg_volume(self): 
        return self.__quote['avgVolume']

    @property   
    def open(self):
        return self.__quote['open']

    @property
    def previous_close(self):
        return self.__quote['previousClose']

    @property
    def eps(self):
        return self.__quote['eps']
   
    @property
    def earnings_announcement(self):
        return self.__quote['earningsAnnouncement']
    
    @property
    def shares_outstanding(self):
        return self.__quote['sharesOutstanding']
    
    @property
    def timestamp(self):
        return self.__quote['timestamp']
    
    
    
#def get_history_crypto(symbol: str, type: str):
#     match time.lower():
#         case ''
#   https://financialmodelingprep.com/api/v3/historical-chart/1min/BTCUSD?apikey=fc9f5e0ac89b400c141ad9f64b91f1de

#     url = (f"https://financialmodelingprep.com/api/v3/{quote}/{symbol}?apikey={settings.API_KEY}")
# =======
# # def get_income_statements(symbol:str,limit,period,):
# >>>>>>> Stashed changes

#     response = urlopen(url, cafile=certifi.where())
#     data = response.read().decode("utf-8")

#     if json.loads(data): # if stock was found
#         return json.loads(data)[0]['price']
#     else:
#         return -1

# query = Query('AAPL')
# print(f"{(query.get_market_cap()):.2f}")


# 1. User commands to do something that requires API information of some kind
# 2. Query object is instantiated
# 3. 