# This code is unfinished, but could be developed further for additional features

import certifi
import json
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
from urllib.request import urlopen
import datetime as dt 

import config


def get_history(interval: str = '5min'):
    match interval:
        case 'daily':
            url = f"https://financialmodelingprep.com/api/v3/historical-price-full/AAPL?apikey={config.API_KEY}"
        case _:
            url = f"https://financialmodelingprep.com/api/v3/historical-chart/{interval}/AAPL?apikey={config.API_KEY}"
  
    data = urlopen(url, cafile=certifi.where()).read().decode('utf-8')
  
    if json.loads(data):
        data_dict = json.loads(data)
        x_points = []
        y_points = []
        for time_slot in data_dict:
            avg = (time_slot['open'] + time_slot['close']) / 2
            y = avg
            datetime_str = time_slot['date'] # THIS NEEDS TO BE CONVERTED TO MDATES FORMAT
            x = dt.datetime.strptime(datetime_str,"%Y-%m-%d %H:%M:%S")
            x_points.append(x)
            y_points.append(y)

        #    Example date string: '2022-05-20 16:00:00'

#             Exception has occurred: ValueError
# time data '2' does not match format '%Y-%m-%d %H:%M:%S'
#   File "C:\Users\aidan\Documents\GitHub\StonkBot\data_plotting.py", line 27, in <listcomp>
#     x = [dt.datetime.strptime(d,'%Y-%m-%d %H:%M:%S').date() for d in dates]
#   File "C:\Users\aidan\Documents\GitHub\StonkBot\data_plotting.py", line 27, in get_history
#     x = [dt.datetime.strptime(d,'%Y-%m-%d %H:%M:%S').date() for d in dates]
#   File "C:\Users\aidan\Documents\GitHub\StonkBot\data_plotting.py", line 41, in plot
#     x_points, y_points = get_history(interval)
#   File "C:\Users\aidan\Documents\GitHub\StonkBot\data_plotting.py", line 58, in <module>
#     plot('15min')

            # year =int(x[0:3])
            # month=int(x[5:6])
            # day = int(x[8:9])

        return x_points, y_points
    else:
        print('error')


def plot(interval: str = '5min'):
    x_points, y_points = get_history(interval)
    #plt.plot(x_points, y_points)

    # plt.xlabel('Time')
    # plt.ylabel('Asset Price ($)')
    # plt.MaxNLocator(20)
    # # plt.figure()
    # plt.show()
    # plt.savefig('plot_figure.png')
    # return 'plot_figure.png'
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=5))
    plt.plot(x_points, y_points)
    plt.gcf().autofmt_xdate()
    plt.show()
    plt.savefig('plot_figure.png')

plot('15min')