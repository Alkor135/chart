# В КВИКе запускаем луа-скрипт QuikLuaPython.lua
# Скрипт для построения дельта графика с отображением кластера с макс объемом

import socket
import threading
from datetime import datetime, timezone
import pandas as pd
import finplot as fplt

fplt.display_timezone = timezone.utc


class DeltaBar:
    def __init__(self):
        self.df = pd.DataFrame(columns='date_time open high low close delta delta_time_sec max_vol_cluster'.split(' '))
        self.df.loc[len(self.df)] = [0, 0, 0, 0, 0, 0, 0, 0]
        self.df_ticks = pd.DataFrame(columns='last vol'.split(' '))

    def max_cluster_calculate(self, price, volume):
        self.df_ticks.loc[len(self.df_ticks)] = [0, 0]  # Добавляем строку
        self.df_ticks.iloc[-1]['last'] = price
        self.df_ticks.iloc[-1]['vol'] = volume
        s_rez = self.df_ticks.groupby('last')['vol'].sum()  # Series (в индексе цена, в значениях суммы объемов)
        # max_clu = s_rez.max()  # Нахождение максимального значения в Series (макс сумма объема в кластере)
        max_idx = s_rez.idxmax()  # Нахождение индекса для максимального значения в Series (соответствует цене)
        return max_idx

    def parser(self, parse):
        if parse[0] == '1' and parse[1] == 'RIH1':
            # Если бар сформирован по дельте и имеет время открытия отличное от времени последней сделки
            if abs(self.df.iloc[-1]['delta']) >= 500:
                # Если время открытия дельта бара отлично от времени последней сделки
                if self.df.iloc[-1]['date_time'] != datetime.strptime(f'{parse[7]} {parse[8][0:-1]}',
                                                                      "%d.%m.%Y %H:%M:%S.%f").replace(microsecond=0):
                    self.df.loc[len(self.df)] = [0, 0, 0, 0, 0, 0, 0, 0]  # Добавляем строку в DF
                    self.df_ticks = self.df_ticks.iloc[0:0]  # Очищаем DF с тиками

            self.df.iloc[-1]['close'] = float(parse[4])  # Записываем последнюю цену как цену close бара

            if self.df.iloc[-1]['date_time'] == 0:  # Если последняя строка имеет нули (начался новый бар)
                # Время последней сделки записываем как время открытия бара
                self.df.iloc[-1]['date_time'] = datetime.strptime(f'{parse[7]} {parse[8][0:-1]}',
                                                                  "%d.%m.%Y %H:%M:%S.%f").replace(microsecond=0)

            if self.df.iloc[-1]['open'] == 0:  # Если цена открытия бара 0
                self.df.iloc[-1]['open'] = float(parse[4])  # Записываем цену последней сделки как цену открытия

            if float(parse[4]) > self.df.iloc[-1]['high']:  # Если цена последней сделки больше чем high
                self.df.iloc[-1]['high'] = float(parse[4])  # Записываем цену последней сделки как high

            # Если цена последней сделки меньше чем low или low равен 0
            if (float(parse[4]) < self.df.iloc[-1]['low']) or \
                    (self.df.iloc[-1]['low'] == 0):
                self.df.iloc[-1]['low'] = float(parse[4])  # Записывем цену последней сделки как low

            if parse[5] == '1026':  # Если последняя сделка была на покупку
                self.df.iloc[-1]['delta'] += float(parse[6])  # Увеличиваем дельту бара на объем посл. сделки

            if parse[5] == '1025':  # Если последняя сделка была на продажу
                self.df.iloc[-1]['delta'] -= float(parse[6])  # Уменьшаем дельту бара на объем посл. сделки

            # Подсчитываем колличество секунд прошедшее от начала бара до последней сделки
            self.df.iloc[-1]['delta_time_sec'] = \
                datetime.strptime(f'{parse[7]} {parse[8][0:-1]}', "%d.%m.%Y %H:%M:%S.%f") - \
                self.df.iloc[-1]['date_time']
            # Записываем колличество секунд формирования бара
            self.df.iloc[-1]['delta_time_sec'] = self.df.iloc[-1]['delta_time_sec'].seconds

            # Записываем цену кластера с максимальным объемом
            self.df.iloc[-1]['max_vol_cluster'] = self.max_cluster_calculate(float(parse[4]), float(parse[6]))


def service():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', 3595))  # Хост-этот компьютер, порт - 3595
    while True:
        res = sock.recv(2048).decode('utf-8')
        if res == '<qstp>\n':  # строка приходит от клиента при остановке луа-скрипта в КВИКе
            break
        else:
            delta_bar.parser(res.split(' '))  # Здесь вызываете свой парсер. Для примера функция: parser (parse)
    sock.close()


def update():
    # if delta_bar.df[-1]['open'] != 0:
    df = delta_bar.df
    # Меняем индекс и делаем его типом datetime
    df = df.set_index(pd.to_datetime(df['date_time'], format='%Y-%m-%d %H:%M:%S'))
    df = df.drop('date_time', 1)  # Удаляем колонку с датой и временем, т.к. дата у нас теперь в индексе
    print(df)

    # pick columns for our three data sources: candlesticks and TD
    candlesticks = df['open close high low'.split()]
    deltabarsec = df['open close delta_time_sec'.split()]
    delta = df['open close delta'.split()]
    maxvolcluster = df['max_vol_cluster']
    if not plots:
        # first time we create the plots
        global ax
        plots.append(fplt.candlestick_ochl(candlesticks))
        plots.append(fplt.volume_ocv(deltabarsec, ax=ax2))
        plots.append(fplt.volume_ocv(delta, ax=ax3))
        plots.append(fplt.plot(maxvolcluster, style='o', color='#00f'))
    else:
        # every time after we just update the data sources on each plot
        plots[0].update_data(candlesticks)
        plots[1].update_data(deltabarsec)
        plots[2].update_data(delta)
        plots[3].update_data(maxvolcluster)


if __name__ == '__main__':
    delta_bar = DeltaBar()
    # Запускаем сервер в своем потоке
    t = threading.Thread(name='service', target=service)
    t.start()

    # print(f'{delta_bar.df[-1]["open"]=}')

    # if delta_bar.df[-1]['open'] != 0:
    plots = []
    ax, ax2, ax3 = fplt.create_plot('RIH1', init_zoom_periods=100, maximize=False, rows=3)
    update()
    fplt.timer_callback(update, 2.0)  # update (using synchronous rest call) every N seconds

    fplt.show()
