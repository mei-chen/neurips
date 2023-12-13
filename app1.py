import streamlit as st
import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine
import os
from openai import OpenAI
from dotenv import load_dotenv
import altair as alt

# Load environment variables
load_dotenv()

# Access your API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

st.set_page_config(layout="wide")
st.title("NeurIPS Poster Search")

# Load CSV files
embeddings_df = pd.read_csv('embedding/embedded_combined1.csv')

# Assuming 'ada_embedding' is a string representation of a list
# Convert it to numpy array
def convert_to_numpy(embedding_str):
    return np.array(embedding_str.strip('[]').split(', '), dtype=float)

embeddings_df['ada_embedding'] = embeddings_df['ada_embedding'].apply(convert_to_numpy)

# Function to get embedding from OpenAI
def get_embedding(text, model="text-embedding-ada-002"):
    response = client.embeddings.create(input=[text], model=model)
    return np.array(response.data[0].embedding)

# UMAP Visualization
df_umap = pd.read_csv('visual/umap_emb.csv')

# User input for search
query = st.text_input("What topics are you interested in?")


# Search functionality
if query:
    query_embedding = get_embedding(query)

    # Calculate cosine similarity with each embedding in the list
    similarity_scores = [1 - cosine(query_embedding, emb) for emb in embeddings_df['ada_embedding']]

    # Combine scores with titles and their indices from your dataset
    scored_titles = list(zip(similarity_scores, embeddings_df['title'], range(len(similarity_scores))))
    scored_titles.sort(key=lambda x: x[0], reverse=True)

    # Display top 6 relevant titles
    for score, title, _ in scored_titles[:6]:
        st.write(f"{title} (Score: {score})")

    # Get indices of top 6 relevant papers
    top_indices = [idx for _, _, idx in scored_titles[:6]]

    # Create a copy of df_umap and add a new column for highlighting
    df_umap_copy = df_umap.copy()
    df_umap_copy['highlight'] = df_umap_copy.index.isin(top_indices)


        # Create and customize the chart with conditional color
    chart = alt.Chart(df_umap_copy).mark_point(size =100, filled=True).encode(
        x=alt.X('x', axis=alt.Axis(title=None)),
        y=alt.Y('y', axis=alt.Axis(title=None)),
        color=alt.condition(
            alt.datum.highlight,  # If the 'highlight' field is True
            alt.value('green'),    # Use red color
            alt.value('lightgray')    # Else, use blue color
        ),
        tooltip=['title']
    ).properties(
        width=600,  # Adjust the width as needed
        height=400  # Adjust the height as needed
    ).configure_axis(
        grid=False,
        labels=False,
        ticks=False,
        domain=False
    )

    st.altair_chart(chart, use_container_width=True)




# Create and customize the chart
# chart = alt.Chart(df_umap).mark_point().encode(
#     x=alt.X('x', axis=alt.Axis(title=None)),
#     y=alt.Y('y', axis=alt.Axis(title=None)),
#     tooltip=['title']
# ).configure_axis(
#     grid=False,
#     labels=False,
#     ticks=False,
#     domain=False
# )

# st.altair_chart(chart, use_container_width=True)


