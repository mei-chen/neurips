'''attach the poster number to the embedding'''

import pandas as pd

combined = pd.read_csv('../data/combined.csv')
embedding = pd.read_csv('embedded_combined1.csv')

print(combined.columns)
print(len(combined))
print(embedding.columns)
print(len(embedding))

# Merge based on the 'title' column
merged_df = embedding.merge(combined[['title', 'poster_number']], on='title', how='left')

# Display the merged DataFrame
print(merged_df.columns)

print(merged_df.head())
print(merged_df['combined'])

merged_df.to_csv('embedded_combined2.csv', index=False)

print(merged_df['poster_number'].describe())