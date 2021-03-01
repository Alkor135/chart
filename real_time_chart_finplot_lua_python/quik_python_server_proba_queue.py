# В КВИКе запускаем луа-скрипт QuikLuaPython.lua
# Проба очереди для исключения потери данных
import socket
import threading
# import queue
from multiprocessing import Queue
from datetime import datetime


def parser(parse):
    if parse[0] == '1' and parse[1] == 'RIH1':  # записываем цену текущего тика RIH1 в список ticks
        print(parse)
        # time = parse[8]
        # print(time[0:-1])
        # print(time)
        # print(parse[8][0:-1])
        # proba_datetime = datetime.strptime(f'{parse[7]}', "%d.%m.%Y").date()
        # print(proba_datetime)


def service():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('127.0.0.1', 3595))  # Хост-этот компьютер, порт - 3595
    while True:
        res = sock.recv(2048).decode('utf-8')
        if res == '<qstp>\n':  # строка приходит от клиента при остановке луа-скрипта в КВИКе
            break
        else:
            # parser(res.split(' '))  # Здесь вызываете свой парсер. Для примера функция: parser (parse)
            parse = res.split(' ')
            if parse[0] == '1' and parse[1] == 'RIH1':
                # print(parse)
                q.put(parse)  # Помещаем в очередь данные от клиента
    sock.close()


q = Queue()
# Запускаем сервер в своем потоке
t = threading.Thread(name='service', target=service)
t.start()

while True:
# while not q.empty():
    print(q.get())
    # parser(q.get())
