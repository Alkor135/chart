# В КВИКе запускаем луа-скрипт QuikLuaPython.lua
# скрипт с сайта jatotrader
import socket
import threading
from datetime import datetime


# ticks=[]
def parser(parse):
    if parse[0] == '1' and parse[1] == 'RIH1':  # записываем цену текущего тика RIH1 в список ticks
        # ticks.append(float(parse[4]))
        print(parse)
        time = parse[8]
        print(time[0:-1])
        print(time)
        print(parse[8][0:-1])
        proba_datetime = datetime.strptime(f'{parse[7]}', "%d.%m.%Y").date()
        # proba_datetime = datetime.strptime(f'{parse[7]} {parse[8][0:-1]}', "%d.%m.%Y %H:%M:%S").date()
        print(proba_datetime)


def service():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', 3587))  # Хост-этот компьютер, порт - 3587
    while True:
        res = sock.recv(2048).decode('utf-8')
        if res == '<qstp>\n':  # строка приходит от клиента при остановке луа-скрипта в КВИКе
            break
        else:
            parser(res.split(' '))  # Здесь вызываете свой парсер. Для примера функция: parser (parse)
            # print(res.split(' '))
    sock.close()


# Запускаем сервер в своем потоке
t = threading.Thread(name='service', target=service)
t.start()
