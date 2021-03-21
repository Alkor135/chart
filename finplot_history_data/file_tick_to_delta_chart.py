# -*- coding: utf-8 -*-
# Из файла с тиками делает дельта график за один день

import pandas as pd
from datetime import datetime, timezone
import finplot as fplt
import time


def index_date_time(df):
    """
    Функция обрабатывает принятый DF, преобразуя колонки с датой и временем в индекс формата Datetime
    :param df: Принимает в качестве аргумента DataFrame
    :return: Возвращает DataFrame с индексом в виде даты и времени
    """
    # Создаем новый столбец date_time слиянием столбцов <DATE> и <TIME>
    df['<DATE_TIME>'] = df['<DATE>'].astype(str) + ' ' + df['<TIME>'].astype(str)

    # Меняем индекс и делаем его типом date
    df = df.set_index(pd.DatetimeIndex(df['<DATE_TIME>']))

    # Удаляем ненужные колонки. '1' означает, что отбрасываем колонку а не индекс
    df = df.drop('<DATE_TIME>', 1)
    df = df.drop('<DATE>', 1)
    df = df.drop('<TIME>', 1)
    df = df.drop('<ID>', 1)

    return df


def app_row_df_delta_bar(df):
    print(df)
    df_delta_bar = df_delta_bar.append(
        pd.DataFrame(
            [[df[0, 'date_time'],
              df[0, 'last'],
              df['last'].max(),
              df['last'].min(),
              df[len(df) - 1, 'last'],
              row['<DELTA>']]],
            columns=['date_time', 'last', 'vol', 'delta']),
        ignore_index=True
    )


def create_df_delta_tick(df, delta_period):
    """
    Функция проходит по DF из тиков и создает в цикле DF одного дельта бара
    :param df:
    :return:
    """
    df['<DELTA>'] = None  # Создаем колонку <DELTA> и заполняем ее None

    # Создаем пустой DF для массива одной дельта свечи
    df_delta_tick = pd.DataFrame(columns=['date_time', 'last', 'vol', 'delta'])

    previous_price = None  # Предыдущая цена
    previous_delta = 0  # Предыдущая дельта
    ask_flag = None  # Флаг Up тика

    max_pr = len(df)
    pr = 0

    for index, row in df.iterrows():  # Перебираем строки в тиковом DF
        print(f"\r{pr * 100 / max_pr:.2f}% за {time.time() - start_time:.0f} секунд", end='')
        pr += 1
        if previous_price is None:  # Если нет предыдущей цены (первая строка в DF)
            previous_price = row['<LAST>']  # Предыдущей ценой будет текущая цена
            continue

        elif previous_price < row['<LAST>']:  # Последняя цена выше чем предыдущая
            row['<DELTA>'] = previous_delta + row['<VOL>']  # В дельту плюсуем объем
            ask_flag = True
            # print(f'Тик вверх {previous_delta=}, {row["delta"]=}')
        elif previous_price > row['<LAST>']:  # Последняя цена ниже чем предыдущая
            row['<DELTA>'] = previous_delta - row['<VOL>']  # Из дельты вычитаем объем
            ask_flag = False
            # print(f'Тик вниз {previous_delta=}, {row["delta"]=}')
        elif (previous_price == row['<LAST>']) and (
                ask_flag is True):  # Последняя цена равна предыдущей, предыдущий тик вверх
            row['<DELTA>'] = previous_delta + row['<VOL>']
        elif (previous_price == row['<LAST>']) and (
                ask_flag is False):  # Последняя цена равна предыдущей, предыдущий тик вниз
            row['<DELTA>'] = previous_delta - row['<VOL>']
        else:
            row['<DELTA>'] = 0
            print('Проверить состояние')

        # print(f'{str(index)}, {row["last"]}, {row["vol"]}, {row["delta"]}')
        # Дописываем строку в df_delta_tick
        df_delta_tick = df_delta_tick.append(
            pd.DataFrame(
                [[str(index), row['<LAST>'], row['<VOL>'], row['<DELTA>']]],
                columns=['date_time', 'last', 'vol', 'delta']),
            ignore_index=True
        )

        previous_price = row['<LAST>']
        previous_delta = row['<DELTA>']

        if abs(row['<DELTA>']) >= delta_period:
            if df_delta_tick.loc[len(df_delta_tick) - 1, 'date_time'] != df_delta_tick.loc[0, 'date_time']:
                app_row_df_delta_bar(df_delta_tick)  # Вызов функции добавления строки в DF с дельта барами
                previous_delta = 0
                # write_delta_file(df_delta_tick, delta_period)
                # print(f"\r{df_delta_tick} ", end='')
                df_delta_tick = df_delta_tick.iloc[0:0]  # Срос всех значений df_delta_tick


if __name__ == '__main__':
    start_time = time.time()
    file_tick = 'c:/Jatotrader/QSCALP/SPFB.RTS-3.21_210201_210201.txt'
    delta_period = 500

    fplt.display_timezone = timezone.utc  # Настройка тайм зоны, чтобы не было смещения времени

    # Настройки для отображения широкого df pandas
    pd.options.display.width = 1200
    pd.options.display.max_colwidth = 100
    pd.options.display.max_columns = 100

    df = pd.read_csv(file_tick)  # Читаем данные из файла в DF
    df = index_date_time(df)  # Пребразование <DATE>  <TIME> в <DATE_TIME>
    # Создаем DF под дельта бары
    df_delta_bar = pd.DataFrame(
        columns=['<DATE_TIME>',
                 '<OPEN>',
                 '<HIGH>',
                 '<LOW>',
                 '<CLOSE>',
                 '<DELTA>',
                 '<SEC>',
                 '<MAX_VOL>']
    )

    create_df_delta_tick(df, delta_period)

    print("--- %s seconds ---" % (time.time() - start_time))
