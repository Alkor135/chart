from datetime import datetime


parse_lst = ['1', 'RIH1', '348044', '1925034127665775668', '144440.0', '1026', '2.0', '18.2.2021', '18:29:41.328\n']

print(parse_lst[8])  # Выводит время(формат str) со знаком окончания строки
print(parse_lst[8][0:-1])  # Выводит время(формат str) без знака окончания строки

# Преобразование в формат datetime
tmp_datetime = datetime.strptime(f'{parse_lst[7]} {parse_lst[8][0:-1]}', "%d.%m.%Y %H:%M:%S.%f")
print(datetime.strptime(f'{parse_lst[7]} {parse_lst[8][0:-1]}', "%d.%m.%Y %H:%M:%S.%f").date())  # Выводит только дату
print(tmp_datetime.date())  # Выводит только дату
print(datetime.strptime(f'{parse_lst[7]} {parse_lst[8][0:-1]}', "%d.%m.%Y %H:%M:%S.%f").time())  # Выводит только время
print(tmp_datetime.time())  # Выводит только время
print(datetime.strptime(f'{parse_lst[7]} {parse_lst[8][0:-1]}', "%d.%m.%Y %H:%M:%S.%f"))  # Выводит дату и время
print(tmp_datetime)  # Выводит дату и время
print()

# Преобразование формата из datetime в строковый формат
print(tmp_datetime.strftime("%d.%m.%Y %H:%M:%S.%f"))
print(tmp_datetime.strftime("%d.%m.%Y"))
print(tmp_datetime.strftime("%H:%M:%S.%f"))
print(tmp_datetime.strftime("%d.%m.%Y %H:%M:%S"))
