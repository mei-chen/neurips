import pandas as pd

df1 = pd.read_csv('sesh1.csv')
df2 = pd.read_csv('sesh2.csv')
df3 = pd.read_csv('sesh3.csv')
df4 = pd.read_csv('sesh4.csv')
df5 = pd.read_csv('sesh5.csv')
df6 = pd.read_csv('sesh6.csv')

# combine the 6 dfs into one

df = pd.concat([df1, df2, df3, df4, df5, df6], ignore_index=True)

df.to_csv('combined.csv', index=False)