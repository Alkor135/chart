# -*- coding: utf-8 -*-
# Из файла с тиками делает дельта график за один день
# Недоделан. Нужно делать в функциональном стиле
import pandas as pd
from datetime import datetime, timezone
import finplot as fplt


class DeltaBarCreate:
    def __init__(self, file_patch, delta_period):
        self.df = pd.read_csv(file_patch)
        self.df_tick = pd.DataFrame(columns='date_time last vol'.split(' '))
        self.delta_period = delta_period

    def run(self):
        self.df['<UP_DOWN>'] = 0
        # self.df['<DELTA>'] = None  # Создание колонки 'delta' и заполнение ее None
        previous_price = None
        previous_delta = 0
        ask_flag = None
        for index, row in self.df.iterrows():
            if previous_price is None:
                previous_price = row['<LAST>']
                continue
            elif previous_price < row['<LAST>']:  # Последняя цена выше чем предыдущая
                row['<UP_DOWN>'] = 1
                ask_flag = True
                # print(f'Тик вверх {previous_delta=}, {row["<DELTA>"]=}')
                print(f"Тик вверх {previous_price=}, {row['<UP_DOWN>']=}")
            elif previous_price > row['<LAST>']:  # Последняя цена ниже чем предыдущая
                row['<UP_DOWN>'] = -1
                ask_flag = False
                # print(f'Тик вниз {previous_delta=}, {row["<DELTA>"]=}')
            elif (previous_price == row['<LAST>']) and (
                    ask_flag is True):  # Последняя цена равна предыдущей, предыдущий тик вверх
                row['<UP_DOWN>'] = 1
            elif (previous_price == row['<LAST>']) and (
                    ask_flag is False):  # Последняя цена равна предыдущей, предыдущий тик вниз
                row['<UP_DOWN>'] = -1
            previous_price = row['<LAST>']


if __name__ == '__main__':
    file_tick = 'c:/Jatotrader/QSCALP/SPFB.RTS-3.21_210201_210201.txt'
    delta_period = 500

    fplt.display_timezone = timezone.utc  # Настройка тайм зоны, чтобы не было смещения времени

    # Настройки для отображения широкого df pandas
    pd.options.display.width = 1200
    pd.options.display.max_colwidth = 100
    pd.options.display.max_columns = 100

    df_deltabar = DeltaBarCreate(file_tick, delta_period)
    df_deltabar.run()
    print(df_deltabar.df)
