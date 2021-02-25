# -*- coding: utf-8 -*-

import pandas as pd
import finplot as fplt
import datetime

fplt.display_timezone = datetime.timezone.utc

symbol = 'RTS'
# Загружаем файл с разделителем ';' в DF
# Формат файла
"""
2019-04-08 10:00:00,121020.0,121220.0,120780.0,121210.0,42,1102
2019-04-08 10:00:42,121210.0,121240.0,121100.0,121100.0,23,546
2019-04-08 10:01:05,121100.0,121180.0,121030.0,121180.0,79,1071
"""
df = pd.read_csv('c:/data_finam_quote_csv/500_delta.csv',
                 names=["date_time",
                        "open",
                        "high",
                        "low",
                        "close",
                        "delta_time",
                        "ticks"],
                 delimiter=',')

# Меняем индекс и делаем его типом datetime
df = df.set_index(pd.to_datetime(df['date_time'], format='%Y-%m-%d %H:%M:%S'))
# print(df)  # Проверка загруженного

# создаем 4 окна
ax, ax2 = fplt.create_plot(symbol, rows=2)

# рисуем свечной график в основном окне
candles = df[['open', 'close', 'high', 'low']]
fplt.candlestick_ochl(candles, ax=ax)

# рисуем график времени дельты свечи
delta_time = df[['open', 'close', 'delta_time']]
fplt.volume_ocv(delta_time, ax=ax2)

fplt.show()
