# В КВИКе запускаем луа-скрипт QuikLuaPython.lua
# рабочий скрипт для построения дельта графика
import socket
import threading
from datetime import datetime, timezone
import pandas as pd
import finplot as fplt

fplt.display_timezone = timezone.utc


class DeltaBar():
    def __init__(self):
        self.df = pd.DataFrame(columns='date_time open high low close delta delta_time_sec'.split(' '))
        self.df.loc[len(self.df)] = [0, 0, 0, 0, 0, 0, 0]

    def parser(self, parse):
        if parse[0] == '1' and parse[1] == 'RIH1':
            if (abs(self.df.iloc[-1]['delta']) >= 500) and (self.df.iloc[-1]['date_time'] != \
                    datetime.strptime(f'{parse[7]} {parse[8][0:-1]}', "%d.%m.%Y %H:%M:%S.%f").replace(microsecond=0)):
                self.df.loc[len(self.df)] = [0, 0, 0, 0, 0, 0, 0]  # Добавляем строку в DF

            self.df.iloc[-1]['close'] = float(parse[4])  # Записываем последнюю цену как цену close бара

            if self.df.iloc[-1]['date_time'] == 0:
                self.df.iloc[-1]['date_time'] = \
                    datetime.strptime(f'{parse[7]} {parse[8][0:-1]}', "%d.%m.%Y %H:%M:%S.%f").replace(microsecond=0)

            if self.df.iloc[-1]['open'] == 0:
                self.df.iloc[-1]['open'] = float(parse[4])

            if float(parse[4]) > self.df.iloc[-1]['high']:
                self.df.iloc[-1]['high'] = float(parse[4])

            if (float(parse[4]) < self.df.iloc[-1]['low']) or \
                    (self.df.iloc[-1]['low'] == 0):
                self.df.iloc[-1]['low'] = float(parse[4])

            if parse[5] == '1026':
                self.df.iloc[-1]['delta'] += float(parse[6])

            if parse[5] == '1025':
                self.df.iloc[-1]['delta'] -= float(parse[6])

            self.df.iloc[-1]['delta_time_sec'] = \
                datetime.strptime(f'{parse[7]} {parse[8][0:-1]}', "%d.%m.%Y %H:%M:%S.%f") - \
                self.df.iloc[-1]['date_time']
            self.df.iloc[-1]['delta_time_sec'] = self.df.iloc[-1]['delta_time_sec'].seconds  # microsecond


def service():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', 3587))  # Хост-этот компьютер, порт - 3587
    while True:
        res = sock.recv(2048).decode('utf-8')
        if res == '<qstp>\n':  # строка приходит от клиента при остановке луа-скрипта в КВИКе
            break
        else:
            delta_bar.parser(res.split(' '))  # Здесь вызываете свой парсер. Для примера функция: parser (parse)
    sock.close()


def update():

    df = delta_bar.df
    # Меняем индекс и делаем его типом datetime
    df = df.set_index(pd.to_datetime(df['date_time'], format='%Y-%m-%d %H:%M:%S'))
    df = df.drop('date_time', 1)  # Удаляем колонку с датой и временем, т.к. дата у нас теперь в индексе
    print(df)

    # pick columns for our three data sources: candlesticks and TD
    candlesticks = df['open close high low'.split()]
    deltabarsec = df['open close delta_time_sec'.split()]
    delta = df['open close delta'.split()]
    if not plots:
        # first time we create the plots
        global ax
        plots.append(fplt.candlestick_ochl(candlesticks))
        # plots.append(fplt.volume_ocv(deltabarsec, ax=ax.overlay()))
        plots.append(fplt.volume_ocv(deltabarsec, ax=ax2))
        plots.append(fplt.volume_ocv(delta, ax=ax3))
    else:
        # every time after we just update the data sources on each plot
        plots[0].update_data(candlesticks)
        plots[1].update_data(deltabarsec)
        plots[2].update_data(delta)


if __name__ == '__main__':
    delta_bar = DeltaBar()
    # Запускаем сервер в своем потоке
    t = threading.Thread(name='service', target=service)
    t.start()

    plots = []
    # ax = fplt.create_plot('RIH1', init_zoom_periods=100, maximize=False)
    ax, ax2, ax3 = fplt.create_plot('RIH1', init_zoom_periods=100, maximize=False, rows=3)
    update()
    fplt.timer_callback(update, 2.0)  # update (using synchronous rest call) every N seconds

    fplt.show()
