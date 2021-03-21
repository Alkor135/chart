import pandas as pd

file_tick = 'c:/Jatotrader/QSCALP/SPFB.RTS-3.21_210201_210201.txt'

df = pd.read_csv(file_tick)
print(df)

# df_200 = df[df['<VOL>'] >= 200]
# print(df_200)
#
# print(df.loc[:, '<TIME>':'<ID>':1])
#
# for i in range(1, len(df), 1):
#     df_tail_100 = df.tail(i)
#     if df_tail_100.iloc[0]['<VOL>'] >= 100:
#         print(df_tail_100)
#         break
#
# for i in range(1, len(df), 1):
#     df_head_300 = df.head(i)
#     if df_head_300.iloc[-1]['<VOL>'] >= 300:
#         print(df_head_300)
#         break

# for i in range(0, len(df), 1):
#     df2 = df.loc[0:i:1, :].copy
#     print(df2)

for i in range(1, len(df), 1):
    df2 = df.loc[i-1:i:1, :]
    # print(df2)
    if df2.loc[i-1, '<LAST>'] > df2.loc[i, '<LAST>']:
        tmp_val = df.loc[i, '<VOL>']
        df.at[i, '<VOL>'] = -1 * tmp_val
    elif (df2.loc[i-1, '<LAST>'] == df2.loc[i, '<LAST>']) and (df2.loc[i-1, '<VOL>'] < 0):
        tmp_val = df.loc[i, '<VOL>']
        df.at[i, '<VOL>'] = -1 * tmp_val
    # print(df2)
print(df)
