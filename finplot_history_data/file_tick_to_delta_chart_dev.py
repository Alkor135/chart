# -*- coding: utf-8 -*-
# Из файла с тиками делает дельта график за один день
import numpy as np
import pandas as pd
from datetime import datetime, timezone
import finplot as fplt
import time


class DeltaBars:
    def __init__(self, file_tick, delta_period):
        self.df_ticks = pd.read_csv(file_tick)  # Читаем тиковые данные из файла в DF
        self.df_delta_ticks = pd.DataFrame(columns='<DATE_TIME> <LAST> <VOL> <DELTA>'.split(' '))
        self.delta_period = delta_period

    def index_date_time(self):
        """
        Функция обрабатывает тиковый DF, преобразуя колонки с датой и временем в индекс формата Datetime и
        удаляет ненужные колонки
        """
        # Создаем новый столбец date_time слиянием столбцов <DATE> и <TIME>
        self.df_ticks['<DATE_TIME>'] = self.df_ticks['<DATE>'].astype(str) + ' ' + self.df_ticks['<TIME>'].astype(str)

        # Меняем индекс и делаем его типом date
        self.df_ticks = self.df_ticks.set_index(pd.DatetimeIndex(self.df_ticks['<DATE_TIME>']))

        # Удаляем ненужные колонки. '1' означает, что отбрасываем колонку а не индекс
        self.df_ticks = self.df_ticks.drop('<DATE_TIME>', 1)
        self.df_ticks = self.df_ticks.drop('<DATE>', 1)
        self.df_ticks = self.df_ticks.drop('<TIME>', 1)
        self.df_ticks = self.df_ticks.drop('<ID>', 1)

    def delta_bar_df_calculate(self):
        pass

    def run(self):
        self.index_date_time()
        print(self.df_ticks)


if __name__ == '__main__':
    file_tick = 'c:/Jatotrader/QSCALP/SPFB.RTS-3.21_210201_210201.txt'
    delta_period = 500

    delta_bar = DeltaBars(file_tick, delta_period)
    delta_bar.run()
