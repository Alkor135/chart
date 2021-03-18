# После запуска сервера в КВИКе запускаем луа-скрипт QuikLuaPython_3599_TCP.lua
# Данные от сервера в обработчик передаются по средствам организации очереди Queue
# Сервер останавливается, когда клиент закрывает соединение
import socket
import threading
from datetime import datetime, timezone
from multiprocessing import Queue
import finplot as fplt
import pandas as pd
import winsound


class DeltaBars:
    def __init__(self):
        # Создаем df под дельта бары
        self.df = pd.DataFrame(columns='date_time open high low close delta sec max_vol'.split(' '))
        self.df.loc[len(self.df)] = [datetime.now().replace(microsecond=0), 0, 0, 0, 0, 0, 0, 0]
        self.df_ticks = pd.DataFrame(columns='last vol'.split(' '))
        print(self.df)

    def max_cluster_calculate(self, price, volume):
        self.df_ticks.loc[len(self.df_ticks)] = [0, 0]  # Добавляем строку в df с тиками
        self.df_ticks.loc[len(self.df_ticks)-1, 'last'] = price
        self.df_ticks.loc[len(self.df_ticks)-1, 'vol'] = volume
        s_rez = self.df_ticks.groupby('last')['vol'].sum()  # Series (в индексе цена, в значениях суммы объемов)
        # max_clu = s_rez.max()  # Нахождение максимального значения в Series (макс сумма объема в кластере)
        max_idx = s_rez.idxmax()  # Нахождение индекса для максимального значения в Series (соответствует цене)
        return max_idx

    def run(self, parse):
        # Если бар сформирован по дельте
        if abs(self.df.loc[len(self.df)-1, 'delta']) >= delta_val:
            # Если время открытия дельта бара отлично от времени последней сделки
            # для исключения на быстром рынке повторений баров с одним временем (для уникального индекса)
            if self.df.loc[len(self.df)-1, 'date_time'] != \
                    datetime.strptime(f'{parse[7]} {parse[8]}', "%d.%m.%Y %H:%M:%S.%f").replace(microsecond=0):
                self.df.loc[len(self.df)] = [0, 0, 0, 0, 0, 0, 0, 0]  # Добавляем строку в DF
                self.df_ticks = self.df_ticks.iloc[0:0]  # Очищаем DF с тиками

        # Заполняем(изменяем) последнюю строку DF с дельта барами --------------------------------------
        self.df.loc[len(self.df)-1, 'close'] = float(parse[4])  # Записываем последнюю цену как цену close бара

        if self.df.loc[len(self.df)-1, 'open'] == 0:  # Если последняя строка имеет нули (начался новый бар)
            # Время последней сделки записываем как время открытия бара
            self.df.loc[len(self.df)-1, 'date_time'] = datetime.strptime(f'{parse[7]} {parse[8]}',
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
        # только в заданный временной период для исключения отрисовки индикатором больших значений
        if 8 < datetime.time(self.df.loc[len(self.df) - 1, 'date_time']).hour < 22:

            self.df.loc[len(self.df)-1, 'sec'] = \
                datetime.strptime(f'{parse[7]} {parse[8]}', "%d.%m.%Y %H:%M:%S.%f") - \
                self.df.loc[len(self.df)-1, 'date_time']

            # Записываем количество секунд формирования бара (отсекаем микросекунды)
            self.df.loc[len(self.df)-1, 'sec'] = self.df.loc[len(self.df)-1, 'sec'].seconds

            # Записываем цену кластера с максимальным объемом
            self.df.loc[len(self.df)-1, 'max_vol'] = self.max_cluster_calculate(float(parse[4]), float(parse[6]))

        # print(self.df)


def parser():
    while True:
        parse = q.get()  # Получаем из очереди данные от клиента
        delta_bars.run(parse)


# Пример TCP сокет-сервера на порту 3599 с постоянным прослушиванием. Клиент подсоединяется один раз и передает
# данные когда угодно. В примере от клиента приходят строки, разделенные символом \n,
# информация в строках разделена пробелами
def service():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 3599))  # Запускаем сервер на локальной машине, порт 3599
    s.listen(5)  # Начинаем прослушивать (до 5 соединений)
    # Принимаем соединения с помощью функции accept. Она ждёт появления входящего соединения и
    # возвращает связанный с ним сокет и адрес подключившегося. Адрес — массив, состоящий из IP-адреса и порта.
    conn, addr = s.accept()
    global client
    client = conn
    tail = b''  # Не уместившееся полностью в буфер сообщение от клиента. В начале - пустая строка.
    while True:  # "вечный" цикл, пока клиент не "отвалится"
        data = conn.recv(1024)  # Принимаем в буфер data(1024 байт) сообщения от клиента
        if not data:  # Если клиент закрыл сокет,
            conn.close()  # то сервер закрывает это соединение и выходит из цикла
            break
        else:
            # Хотя клиент и отсылает сообщения по одному, разделяя их символом \n, но если идет большой поток сообщений
            # в цикле, то в буфер могут попасть несколько сообщений одновременно
            messages = data.splitlines()  # по-этому, разделяем сообщения в буфере на строки
            # Если на момент обработки буфера присутствует "хвост" от прошлого сообщения
            # (т.е. оно не уместилось целиком в буфере),
            messages[0] = tail + messages[0]  # добавляем его в начало первого сообщения в буфере
            # Если последним элементом в буфере является символ новой строки \n, то все сообщения уместились в буфере
            if data[-1] == 10:  # 10 - это байт-код символа новой строки \n
                tail = b''  # В этом случае "хвостов" не осталось
            else:  # а если сообщение не уместилось в буфер,
                tail = messages[-1]  # то сохраняем этот кусок(последний элемент) как tail
                messages = messages[:-1]  # а сами сообщения сохраняем, но без последнего "обрезка"
            # С этого места можно обрабатывать список сообщений от клиента с гарантией,
            # что все сообщения целы и не обрезаны буфером
            # print('Clear:', messages)
            for m in messages:
                mess = m.decode()  # переводим из бинарной кодировки в utf8
                # print(mess)
                mess = mess.split(' ')
                if mess[0] == '1' and mess[1] == ticker:
                    q.put(mess)  # Помещаем в очередь данные от клиента

    conn.close()  # если клиент закрыл соединение то и мы закрываем соединение
    s.close()


def update():
    df = delta_bars.df
    # Меняем индекс и делаем его типом datetime
    df = df.set_index(pd.to_datetime(df['date_time'], format='%Y-%m-%d %H:%M:%S'))
    df = df.drop('date_time', 1)  # Удаляем колонку с датой и временем, т.к. дата у нас теперь в индексе

    winsound.PlaySound('bite.wav', winsound.SND_FILENAME)

    # print(df)


    # pick columns for our three data sources: candlesticks and TD
    candlesticks = df['open close high low'.split()]
    deltabarsec = df['open close sec'.split()]
    delta = df['open close delta'.split()]
    maxvolcluster = df['max_vol']
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
    # Изменяемые настройки
    ticker = 'RIH1'
    delta_val = 500

    client = None
    fplt.display_timezone = timezone.utc  # Настройка тайм зоны, чтобы не было смещения времени

    # Настройки для отображения широкого df pandas
    pd.options.display.width = 1200
    pd.options.display.max_colwidth = 100
    pd.options.display.max_columns = 100

    delta_bars = DeltaBars()  # Создаем экземпляр класса DeltaBar
    q = Queue()  # Создаем очередь
    # Запускаем сервер в своем потоке
    print('Info: Запуск клиента нужно производить после запуска сервера!')
    t = threading.Thread(name='service', target=service)
    t.start()

    # Запускаем парсер в своем потоке
    t_parser = threading.Thread(name='parser', target=parser)
    t_parser.start()

    plots = []
    ax, ax2, ax3 = fplt.create_plot(ticker, init_zoom_periods=100, maximize=False, rows=3)
    ax.set_visible(xgrid=True, ygrid=True)
    ax2.set_visible(xgrid=True, ygrid=True)
    update()
    fplt.timer_callback(update, 2.0)  # update (using synchronous rest call) every N seconds

    fplt.show()
