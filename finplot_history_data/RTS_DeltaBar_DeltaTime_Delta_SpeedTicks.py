# -*- coding: utf-8 -*-

import pandas as pd
import finplot as fplt
import datetime

fplt.display_timezone = datetime.timezone.utc

symbol = 'RTS'
# Загружаем файл в DF
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

print(df)

df['speed_ticks'] = 0
df['speed_ticks'] = df['delta_time'] / df['ticks']

print(df)
