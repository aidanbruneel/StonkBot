import datetime
from xml.sax.handler import property_declaration_handler
import fmp_api as api

class Asset:
    def __init__(self, ticker: str, quantity = 0):
        # Initialize variables
        self.__ticker = ticker
        self.quantity = quantity
    
    # __ticker property
    @property
    def ticker(self):
        print("Getting ticker...")
        return self.__ticker

class CryptoAsset(Asset):
    def __init__(self, ticker: str, quantity: float = 0.00):
        Asset.__init__(self, ticker, float(quantity))
        self.__type = 'crypto'

class StockAsset(Asset):
   def __init__(self, ticker: str, quantity: int = 0):
       Asset.__init__(self, ticker, int(quantity))
       self.__type = 'stock'

class Receipt:
    def __init__(self, asset: Asset, fee = 0):
        # Initialize variables
        self.__asset: Asset = asset
        self.__quantity = self.__asset.quantity
        match self.__quantity > 0:
            case True:
                self.__type: str = 'sell'
            case False:
                self.__type: str = 'buy'
        self.__time = datetime.datetime.now()
        self.__price = round(api.get_price(asset.ticker), 2)
        self.__fee: float = round(fee, 2)

    # __fee property
    @property
    def fee(self):
        print("Getting fee...")
        return self.__fee

    # __asset property
    @property
    def asset(self):
        print("Getting asset...")
        return self.__asset

    # __time property
    @property
    def time(self):
        print("Getting time...")
        return self.__time
    
    # __price property
    @property
    def price(self):
        print("Getting price...")
        return self.__price

# class Portfolio:
#     def __init__(self, start_cash: float, start_assets = []):
#         # Initialize variables
#         self.cash = start_cash
#         self.assets = start_assets
#         self.receipts = []
    
#     def adjust_cash(self, change: float):
#         self.cash += round(change, 2)

#     def adjust_asset(self, ticker: str):
#         print('hi')