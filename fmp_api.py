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
        return -1


# def get_income_statements(ticker:str,limit,period,):

# def get_daily_prices(ticker:str,timeseries):
#     url = (f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?apikey={API_KEY}")

# def get_key_metrics(ticker:str, limit, API_key,period):
#     url = (f"https://financialmodelingprep.com/api/v3")
