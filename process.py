'combines the sesh1-6 csv files into one csv file'

import pandas as pd

df1 = pd.read_csv('data/sesh1.csv')
df2 = pd.read_csv('data/sesh2.csv')
df3 = pd.read_csv('data/sesh3.csv')
df4 = pd.read_csv('data/sesh4.csv')
df5 = pd.read_csv('data/sesh5.csv')
df6 = pd.read_csv('data/sesh6.csv')

df1['session'] = 1
df2['session'] = 2
df3['session'] = 3
df4['session'] = 4
df5['session'] = 5
df6['session'] = 6

# combine the 6 dfs into one
df = pd.concat([df1, df2, df3, df4, df5, df6], ignore_index=True)

df.to_csv('data/combined.csv', index=False)