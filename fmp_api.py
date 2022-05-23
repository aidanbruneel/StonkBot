from urllib.request import urlopen
import certifi
import json
import config
import matplotlib.pyplot as plt 


#from  data_plotting import plot # might not need this
import config

class Query:
    def __init__(self, symbol: str):
        self.__symbol = symbol
        # Quote
        self.__quote = self.get_quote()
        self.__profile = self.get_profile()

    def web_scrape(self, url: str): # Returns dict
        data = urlopen(url, cafile=certifi.where()).read().decode('utf-8')

        if json.loads(data): # if symbol was found
            return json.loads(data)[0]
        else:
            return None

    def get_quote(self):
        url = (f"https://financialmodelingprep.com/api/v3/quote/{self.__symbol}?apikey={config.API_KEY}")
        return self.web_scrape(url)

    def get_profile(self):
        url = (f"https://financialmodelingprep.com/api/v3/profile/{self.__symbol}?apikey={config.API_KEY}")
        return self.web_scrape(url)
    
    def get_history(self, interval: str):
        match interval:
            case 'daily':
                url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{self.__symbol}?apikey={config.API_KEY}"
            case _:
                url = f"https://financialmodelingprep.com/api/v3/historical-price/{interval}/{self.__symbol}?apikey={config.API_KEY}"
        
        data = urlopen(url, cafile=certifi.where()).read().decode('utf-8')
        
        if json.loads(data):
            data_dict = json.loads(data)
            y = []
            for time_slot in data_dict:
                avg = (time_slot['open'] + time_slot['close']) / 2
                y.append(avg)
            return y
        else:
            print('error')
            return None

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
    def symbol(self):
        return self.__symbol

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
    
    def plot(self, interval: str = '5min'):
        y = self.get_history(interval)
        x = [i for i in range(1, len(y) + 1)]
        plt.plot(x,y)
        plt.xlabel('time')
        plt.ylabel('stock price')
        plt.figure()
        plt.show()
        plt.savefig('plot_figure.png')
        return 'plot_figure.png'
