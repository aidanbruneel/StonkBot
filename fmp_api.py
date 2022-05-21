from urllib.request import urlopen
import certifi
import json
# import matplotlib.pyplot as plt

import settings

def get_price(ticker: str, type: str):
    match type.lower():
        case 'stock':
            quote = 'quote-short'
        case 'crypto':
            quote = 'quote'
    
    url = (f"https://financialmodelingprep.com/api/v3/{quote}/{ticker}?apikey={settings.API_KEY}")

    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")

    if json.loads(data): # if stock was found
        return json.loads(data)[0]['price']
    else:
        return None

def get_company_price_change(ticker:str):
    url = (f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={settings.API_KEY}")
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")

    if json.loads(data): # if stock was found
        return json.loads(data)[0]['change']
    else:
        return None
 
def get_company_market_cap(ticker:str):
    url = (f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={settings.API_KEY}")
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")

    if json.loads(data): # if stock was found
        return json.loads(data)[0]['marketCap']
    else:
        return None

def get_company_price-earings_ratio(ticker:str):
    url = (f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={settings.API_KEY}")
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")

    if json.loads(data): # if stock was found
        return json.loads(data)[0]['pe']
    else:
        return None



"""def get_history_crypto(ticker: str, type: str):
    match time.lower():
        case ''
  https://financialmodelingprep.com/api/v3/historical-chart/1min/BTCUSD?apikey=fc9f5e0ac89b400c141ad9f64b91f1de

    url = (f"https://financialmodelingprep.com/api/v3/{quote}/{ticker}?apikey={settings.API_KEY}")

    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")

    if json.loads(data): # if stock was found
        return json.loads(data)[0]['price']
    else:
        return -1"""

