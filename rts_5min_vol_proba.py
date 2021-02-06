# -*- coding: utf-8 -*-
import pandas as pd
import finplot as fplt

symbol = 'RTS'
# Загружаем файл с разделителем ';' в DF
# Формат файла
"""
date_time;date;time;open;high;low;close;vol
2019-01-03 10:00:00;20190103.0;100000.0;106580.0;107280.0;106570.0;107060.0;8517.0
2019-01-03 10:05:00;20190103.0;100500.0;107050.0;107150.0;106770.0;106790.0;3926.0
2019-01-03 10:10:00;20190103.0;101000.0;106790.0;107060.0;106730.0;106990.0;2184.0
"""
df = pd.read_csv('c:/data_prepare_quote_csv/SPFB.RTS_5min.csv', delimiter=';')
# Меняем индекс и делаем его типом datetime
df = df.set_index(pd.to_datetime(df['date_time'], format='%Y-%m-%d %H:%M:%S'))

# Получение строк по диапазону дат
# df = df.query("'2020-02-10' <= date_time < '2020-02-11'")

# create axes
ax = fplt.create_plot(symbol, rows=1)

# plot candle sticks
candles = df[['open', 'close', 'high', 'low']]  # 'date_time',
fplt.candlestick_ochl(candles, ax=ax)

# overlay volume on the top plot
volumes = df[['open', 'close', 'vol']]  # 'date_time',
fplt.volume_ocv(volumes, ax=ax.overlay())

fplt.show()
