# -*- coding: utf-8 -*-
# Из файла с тиками делает дельта график за один день
# Недоделан
import pandas as pd


class DeltaBarCreate:
    def __init__(self, file_patch, delta_period):
        self.df = pd.read_csv(file_patch)
        self.df_tick = pd.DataFrame(columns='date_time last vol'.split(' '))
        self.delta_period = delta_period




if __name__ == '__main__':
    file_tick = 'c:/Jatotrader/QSCALP/SPFB.RTS-3.21_210201_210201.txt'
    delta_period = 500
    DeltaBarCreate(file_tick, delta_period)
