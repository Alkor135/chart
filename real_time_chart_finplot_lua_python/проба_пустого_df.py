import pandas as pd

df = pd.DataFrame(columns='date_time open high low close delta delta_time_sec max_vol_cluster'.split(' '))
print(df)
print(len(df))
