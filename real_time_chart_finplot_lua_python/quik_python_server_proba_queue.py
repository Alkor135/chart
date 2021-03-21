# В КВИКе запускаем луа-скрипт QuikLuaPython.lua
# Проба очереди для исключения потери данных
import socket
import threading
import pandas as pd
from multiprocessing import Queue
from datetime import datetime, timezone
import finplot as fplt

fplt.display_timezone = timezone.utc  # Настройка тайм зоны, чтобы не было смещения времени


class DeltaBars:
    def __init__(self):
        # Создаем df под дельта бары
        self.df = pd.DataFrame(columns='date_time open high low close delta delta_time_sec max_vol_cluster'.split(' '))
        self.df.loc[len(self.df)] = [datetime.now().replace(microsecond=0), 0, 0, 0, 0, 0, 0, 0]
        self.df_ticks = pd.DataFrame(columns='last vol'.split(' '))
        print(self.df)

    def max_cluster_calculate(self, price, volume):
        self.df_ticks.loc[len(self.df_ticks)] = [0, 0]  # Добавляем строку
        # self.df_ticks.iloc[-1]['last'] = price
        # self.df_ticks.iloc[-1]['vol'] = volume
        self.df_ticks.loc[len(self.df_ticks)-1, 'last'] = price
        self.df_ticks.loc[len(self.df_ticks)-1, 'vol'] = volume
        s_rez = self.df_ticks.groupby('last')['vol'].sum()  # Series (в индексе цена, в значениях суммы объемов)
        # max_clu = s_rez.max()  # Нахождение максимального значения в Series (макс сумма объема в кластере)
        max_idx = s_rez.idxmax()  # Нахождение индекса для максимального значения в Series (соответствует цене)
        return max_idx

    def run(self, parse):
        # Если бар сформирован по дельте
        if abs(self.df.loc[len(self.df)-1, 'delta']) >= 500:
            # Если время открытия дельта бара отлично от времени последней сделки
            if self.df.loc[len(self.df)-1, 'date_time'] != \
                    datetime.strptime(f'{parse[7]} {parse[8][0:-1]}', "%d.%m.%Y %H:%M:%S.%f").replace(microsecond=0):
                self.df.loc[len(self.df)] = [0, 0, 0, 0, 0, 0, 0, 0]  # Добавляем строку в DF
                self.df_ticks = self.df_ticks.iloc[0:0]  # Очищаем DF с тиками

        self.df.loc[len(self.df)-1, 'close'] = float(parse[4])  # Записываем последнюю цену как цену close бара

        if self.df.loc[len(self.df)-1, 'open'] == 0:  # Если последняя строка имеет нули (начался новый бар)
            # Время последней сделки записываем как время открытия бара
            self.df.loc[len(self.df)-1, 'date_time'] = datetime.strptime(f'{parse[7]} {parse[8][0:-1]}',
                                                                         "%d.%m.%Y %H:%M:%S.%f").replace(microsecond=0)
            self.df.loc[len(self.df)-1, 'open'] = float(parse[4])  # Записываем цену последней сделки как цену открытия

        if float(parse[4]) > self.df.loc[len(self.df)-1, 'high']:  # Если цена последней сделки больше чем high
            self.df.loc[len(self.df)-1, 'high'] = float(parse[4])  # Записываем цену последней сделки как high

        # Если цена последней сделки меньше чем low или low равен 0
        if (float(parse[4]) < self.df.loc[len(self.df)-1, 'low']) or \
                (self.df.loc[len(self.df)-1, 'low'] == 0):
            self.df.loc[len(self.df)-1, 'low'] = float(parse[4])  # Записываем цену последней сделки как low

        if parse[5] == '1026':  # Если последняя сделка была на покупку
            self.df.loc[len(self.df)-1, 'delta'] += float(parse[6])  # Увеличиваем дельту бара на объем посл. сделки

        if parse[5] == '1025':  # Если последняя сделка была на продажу
            self.df.loc[len(self.df)-1, 'delta'] -= float(parse[6])  # Уменьшаем дельту бара на объем посл. сделки

        # Подсчитываем количество секунд прошедшее от начала бара до последней сделки
        self.df.loc[len(self.df)-1, 'delta_time_sec'] = \
            datetime.strptime(f'{parse[7]} {parse[8][0:-1]}', "%d.%m.%Y %H:%M:%S.%f") - \
            self.df.loc[len(self.df)-1, 'date_time']

        # Записываем количество секунд формирования бара (отсекаем микросекунды)
        self.df.loc[len(self.df)-1, 'delta_time_sec'] = self.df.loc[len(self.df)-1, 'delta_time_sec'].seconds

        # Записываем цену кластера с максимальным объемом
        self.df.loc[len(self.df)-1, 'max_vol_cluster'] = self.max_cluster_calculate(float(parse[4]), float(parse[6]))
        print(self.df)


def parser():
    while True:
        parse = q.get()  # Получаем из очереди данные от клиента
        delta_bars.run(parse)


def service():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', 3595))  # Хост-этот компьютер, порт - 3595
    while True:
        res = sock.recv(2048).decode('utf-8')
        if res == '<qstp>\n':  # строка приходит от клиента при остановке луа-скрипта в КВИКе
            break
        else:
            pars = res.split(' ')  # Данные от клинта разбиваем на элементы и помещаем в словарь
            if pars[0] == '1' and pars[1] == 'RIH1':
                q.put(pars)  # Помещаем в очередь данные от клиента
    sock.close()


def update():
    df = delta_bars.df
    # Меняем индекс и делаем его типом datetime
    df = df.set_index(pd.to_datetime(df['date_time'], format='%Y-%m-%d %H:%M:%S'))
    df = df.drop('date_time', 1)  # Удаляем колонку с датой и временем, т.к. дата у нас теперь в индексе
    # print(df)

    # pick columns for our three data sources: candlesticks and TD
    candlesticks = df['open close high low'.split()]
    deltabarsec = df['open close delta_time_sec'.split()]
    delta = df['open close delta'.split()]
    maxvolcluster = df['max_vol_cluster']
    if not plots:
        # first time we create the plots
        global ax
        plots.append(fplt.candlestick_ochl(candlesticks, candle_width=0.8))
        plots.append(fplt.volume_ocv(deltabarsec, ax=ax2))
        fplt.add_legend('Время формирования бара', ax=ax2)
        plots.append(fplt.volume_ocv(delta, colorfunc=fplt.strength_colorfilter, ax=ax3))
        fplt.add_legend('Дельта', ax=ax3)
        plots.append(fplt.plot(maxvolcluster, legend='Max volume', style='o', color='#00f'))
    else:
        # every time after we just update the data sources on each plot
        plots[0].update_data(candlesticks)
        plots[1].update_data(deltabarsec)
        plots[2].update_data(delta)
        plots[3].update_data(maxvolcluster)


if __name__ == '__main__':
    # Настройки для отображения широкого df pandas
    pd.options.display.width = 1200
    pd.options.display.max_colwidth = 100
    pd.options.display.max_columns = 100

    delta_bars = DeltaBars()  # Создаем экземпляр класса DeltaBar
    q = Queue()  # Создаем очередь
    # Запускаем сервер в своем потоке
    t = threading.Thread(name='service', target=service)
    t.start()

    # Запускаем парсер в своем потоке
    t_parser = threading.Thread(name='parser', target=parser)
    t_parser.start()

    plots = []
    ax, ax2, ax3 = fplt.create_plot('RIH1', init_zoom_periods=100, maximize=False, rows=3)
    ax.set_visible(xgrid=True, ygrid=True)
    ax2.set_visible(xgrid=True, ygrid=True)
    update()
    fplt.timer_callback(update, 2.0)  # update (using synchronous rest call) every N seconds

    fplt.show()
