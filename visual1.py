import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
import plotly.express as px
from ast import literal_eval
import umap

import altair as alt



df = pd.read_csv('embedded_combined.csv')

# Convert the string representations to actual lists
df['ada_embedding'] = df['ada_embedding'].apply(literal_eval)


# Convert the list of embeddings into a NumPy array
embeddings = np.array(df['ada_embedding'].tolist())

# Apply PCA to reduce to 2 dimensions
# pca = PCA(n_components=2)
# reduced_embeddings = pca.fit_transform(embeddings)

# Create a DataFrame for the reduced embeddings
# reduced_df = pd.DataFrame(reduced_embeddings, columns=['PCA1', 'PCA2'])

reducer = umap.UMAP(n_neighbors=7)
umap_embeddings = reducer.fit_transform(np.array(embeddings))


df['x'] = umap_embeddings[:,0]
df['y'] = umap_embeddings[:,1]

# reduced_df = pd.DataFrame(reduced_embeddings, columns=['x', 'y'])

# Assuming you have a 'title' or 'te    xt' column in your DataFrame
# reduced_df['title'] = df['title']  # or df['text'] if you have a text column


# # Create an interactive scatter plot
# fig = px.scatter(df, x='x', y='y', hover_data=['title'], title='Neurips Poster Embeddings')

# # Update hover template to show only the title
# fig.update_traces(hovertemplate='<br>'.join(['%{customdata[0]}']))

# # Increase the text size of the hover labels
# fig.update_layout(hoverlabel=dict(font_size=33))  # You can adjust the font size as needed


# fig.show()

# Assuming df is your DataFrame with columns 'x', 'y', and 'title'
chart = alt.Chart(df[['x', 'y', 'title']]).mark_circle(size=60).encode(
    x='x',
    y='y',
    tooltip=['title']
).properties(
    width=600,
    height=400,
    title='Neurips Poster Embeddings'
)

chart.save('chart.html')

############ SAVE SELECT DF

# Specify the names of the four columns you want to save
columns_to_save = ['x', 'y', 'title', 'abstract']

# Select these columns from the DataFrame
df_selected = df[columns_to_save]

# Save the selected columns to a CSV file
csv_filename = 'visual/umap_emb.csv'  # Replace with your desired file path
df_selected.to_csv(csv_filename, index=False)
