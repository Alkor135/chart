import datetime
import time

now = datetime.datetime.now()

print(now)
print(f"{str(now)} - Текущая дата и время с использованием метода str")

print("Текущая дата и время с использованием атрибутов:")
print(f"{now.year} - Текущий год")
print(f"{now.month} - Текущий месяц")
print(f"{now.day} - Текущий день")
print(f"{now.hour} - Текущий час")
print(f"{now.minute} - Текущая минута")
print(f"{now.second} - Текущая секунда")
print(f"{now.microsecond} - Текущая микросекунда")
print()
print("Текущая дата и время с использованием strftime:")
print(f'{now.strftime("%d-%m-%Y %H:%M")}')
print(f'{now.strftime("%d-%m-%Y %H:%M:%S")}')
print(f'{now.strftime("%Y-%m-%d %H:%M:%S.%f")}')
print()
print("Текущая дата и время с использованием isoformat:")
print(f'{now.isoformat()}')

print()
print(f'{datetime.datetime.today()} - текущая дата и время.')  # текущая дата и время.
print(f'{datetime.datetime.fromtimestamp(time.time())} - дата из стандартного представления времени.')

print(f'{datetime.datetime.date(now)} - объект даты (с отсечением времени).')
print(f'{datetime.datetime.time(now)} - объект времени (с отсечением даты).')
# print(f'{datetime.datetime.combine(date, time)} - объект datetime из комбинации объектов date и time.')
#
# print(datetime.replace([year[, month[, day[, hour[, minute[, second[, microsecond[, tzinfo]]]]]]]]) - возвращает новый объект datetime с изменёнными атрибутами.
#
# print(datetime.weekday() - день недели в числовом формате, понедельник - 0, воскресенье - 6.
#
# print(datetime.isoweekday() - день недели в числовом формате, понедельник - 1, воскресенье - 7.
#
# print(datetime.strptime(date_string, format) - преобразует строку в datetime.
#
# print(datetime.strftime(format) - преобразует datetime в строку в datetime.

print(f'{time.time()} - количество секунд прошедших с 00:00:00 1 января 1970')
print(f'{int(time.time())} - количество секунд прошедших с 00:00:00 1 января 1970')
