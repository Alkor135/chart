# -*- coding: utf-8 -*-

import pandas as pd
import finplot as fplt
import datetime

fplt.display_timezone = datetime.timezone.utc

symbol = 'RTS'
# Загружаем файл с разделителем ';' в DF
# Формат файла
"""
2019-05-08 10:00:00,121100.0,121420.0,121100.0,121420.0,0,145,541
2019-05-08 10:00:00,121430.0,121470.0,121240.0,121400.0,0,141,511
2019-05-08 10:00:00,121400.0,121440.0,121240.0,121330.0,893,5390,501
"""
df = pd.read_csv('c:/data_finam_quote_csv/500_delta_2021.csv',
                 names=["date_time",
                        "open",
                        "high",
                        "low",
                        "close",
                        "delta_time",
                        "ticks",
                        "delta"],
                 delimiter=',')

# Меняем индекс и делаем его типом datetime
df = df.set_index(pd.to_datetime(df['date_time'], format='%Y-%m-%d %H:%M:%S'))
# print(df)  # Проверка загруженного

# создаем 4 окна
ax, ax2, ax3 = fplt.create_plot(symbol, rows=3)

# рисуем свечной график в основном окне
candles = df[['open', 'close', 'high', 'low']]
fplt.candlestick_ochl(candles, ax=ax)

# рисуем график времени дельты свечи
delta_time = df[['open', 'close', 'delta_time']]
fplt.volume_ocv(delta_time, ax=ax2)

# рисуем график дельты
delta = df[['open', 'close', 'delta']]
fplt.volume_ocv(delta, ax=ax3)

fplt.show()
