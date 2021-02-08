# -*- coding: utf-8 -*-

import pandas as pd
import finplot as fplt
import talib

symbol = 'RTS'
# Загружаем файл с разделителем ';' в DF
# Формат файла
"""
2019-04-08 10:00:00,121020.0,121220.0,120780.0,121210.0,42,1102
2019-04-08 10:00:42,121210.0,121240.0,121100.0,121100.0,23,546
2019-04-08 10:01:05,121100.0,121180.0,121030.0,121180.0,79,1071
"""
df = pd.read_csv('c:/data_finam_quote_csv/500_delta.csv', names=["date_time",
                                                                 "open",
                                                                 "high",
                                                                 "low",
                                                                 "close",
                                                                 "delta_time",
                                                                 "ticks"], delimiter=',')

# Меняем индекс и делаем его типом datetime
df = df.set_index(pd.to_datetime(df['date_time'], format='%Y-%m-%d %H:%M:%S'))
# print(df)  # Проверка загруженного

# добавим к DF столбец с WPR 14
df['wpr_1'] = talib.WILLR(df['high'].values, df['low'].values, df['close'].values, timeperiod=14)
# print(df)

# добавим к DF столбец с WPR 96
df['wpr_2'] = talib.WILLR(df['high'].values, df['low'].values, df['close'].values, timeperiod=96)
df['line'] = -50  # Добавляю колонку с линией для индикаторов
print(df)

# создаем 4 окна
ax, ax2, ax3, ax4 = fplt.create_plot(symbol, rows=4)

# рисуем свечной график в основном окне
candles = df[['open', 'close', 'high', 'low']]
fplt.candlestick_ochl(candles, ax=ax)

# рисуем график времени дельты свечи
delta_time = df[['open', 'close', 'delta_time']]
fplt.volume_ocv(delta_time, ax=ax2)

# рисуем график количества тиков
ticks = df[['open', 'close', 'ticks']]
fplt.volume_ocv(ticks, ax=ax3)

# WPR
df[['wpr_1']].plot(ax=ax4, legend='WPR14', color='#008800')
df[['wpr_2']].plot(ax=ax4, legend='WPR96', color='#EF5350')
df[['line']].plot(ax=ax4, color='#000000')  # Построение центральной линии для индикаторов

fplt.show()
