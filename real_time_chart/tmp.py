
import math
import pandas as pd
import finplot as fplt
import requests
import time


# load data
limit = 500
start = int(time.time()*1000) - (500-2)*60*1000
url = 'https://api.bitfinex.com/v2/candles/trade:1m:tBTCUSD/hist?limit=%i&sort=1&start=%i' % (limit, start)
table = requests.get(url).json()
df = pd.DataFrame(table, columns='time open close high low volume'.split())
print(df)
