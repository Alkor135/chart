# В КВИКе запускаем луа-скрипт QuikLuaPython.lua
import socket
import threading
from datetime import datetime
import time


class DeltaBar():
    def __init__(self):
        self.time = 0
        self.open = 0
        self.high = 0
        self.low = 0
        self.close = 0
        self.delta = 0
        self.delta_time_sec = 0

    def parser(self, parse):
        # print(parse)
        if parse[0] == '1' and parse[1] == 'RIH1':
            self.close = float(parse[4])  # Записываем последнюю цену как цену close бара

            if self.time == 0:
                self.time = datetime.strptime(f'{parse[7]} {parse[8][0:-1]}', "%d.%m.%Y %H:%M:%S.%f")
                # self.time = time.time()
            if self.open == 0:
                self.open = float(parse[4])
            if float(parse[4]) > self.high:
                self.high = float(parse[4])
            if (float(parse[4]) < self.low) or (self.low == 0):
                self.low = float(parse[4])

            # quantity = int(parse[6])
            if parse[5] == '1026':
                self.delta += float(parse[6])
                # self.delta += quantity
            if parse[5] == '1025':
                self.delta -= float(parse[6])
                # self.delta -= quantity
            self.delta_time_sec = datetime.strptime(f'{parse[7]} {parse[8][0:-1]}', "%d.%m.%Y %H:%M:%S.%f") - self.time
            # self.delta_time_sec = time.time() - self.time

            print(f'{self.time}, '
                  f'{self.open=}, '
                  f'{self.high=}, '
                  f'{self.low=}, '
                  f'{self.close=}, '
                  f'{self.delta=}, '
                  # f'{self.delta_time_sec.seconds}')
                  f'{self.delta_time_sec.seconds}')


def service():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', 3587))  # Хост-этот компьютер, порт - 3587
    while True:
        res = sock.recv(2048).decode('utf-8')
        if res == '<qstp>\n':  # строка приходит от клиента при остановке луа-скрипта в КВИКе
            break
        else:
            delta_bar.parser(res.split(' '))  # Здесь вызываете свой парсер. Для примера функция: parser (parse)
            # print(res.split(' '))
    sock.close()


delta_bar = DeltaBar()
# Запускаем сервер в своем потоке
t = threading.Thread(name='service', target=service)
t.start()

