from datetime import datetime
import pandas as pd


parse_lst = ['1', 'RIH1', '348044', '1925034127665775668', '144440.0', '1026', '2.0', '18.2.2021', '18:29:41.328\n']

print(parse_lst[8][0:-1])  # Выводит время(формат str) без знака окончания строки

# Преобразование в формат datetime
tmp_datetime = datetime.strptime(f'{parse_lst[7]} {parse_lst[8][0:-1]}', "%d.%m.%Y %H:%M:%S.%f")

# df = pd.DataFrame(columns='date_time open high low close delta_time_sec'.split(' '))
df = pd.DataFrame(columns='date_time open high low close delta_time_sec'.split(' '))
# df = df.set_index(pd.to_datetime(df['date_time'], format='%d-%m-%Y %H:%M:%S.%f'))
df.loc[len(df)] = [0, 0, 0, 0, 0, 0]
print(df)
print()


# df.iloc[len(df) - 1]['date_time'] = f'{parse_lst[7]} {parse_lst[8][0:-1]}'
df.iloc[len(df) - 1]['date_time'] = tmp_datetime
# df.iloc[len(df) - 1].index = tmp_datetime
# df.iloc[len(df) - 1].index = f'{parse_lst[7]} {parse_lst[8][0:-1]}'
df.iloc[len(df) - 1]['open'] = float(parse_lst[4])
                   # float(parse_lst[4]),
                   # float(parse_lst[4]),
                   # float(parse_lst[4]),
df.iloc[len(df) - 1]['delta_time_sec'] = 'дельта_тайм'
print(df)
print()

df.iloc[len(df) - 1] = [f'{parse_lst[7]} {parse_lst[8][0:-1]}',
                   float(parse_lst[4]),
                   float(parse_lst[4]),
                   float(parse_lst[4]),
                   float(parse_lst[4]),
                   'дельта_тайм']
print(df)
