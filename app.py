import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from scipy.spatial.distance import cosine
import csv
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
# Access your API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(
   api_key=OPENAI_API_KEY,
)

st.set_page_config(layout="wide")


st.title("NeurIPS Poster Search")


############ LOAD EMBEDDING ############
# Load the list of embeddings
embeddings_df = pd.read_csv('embedding/embedded_combined1.csv')
# embeddings_list = embeddings_df.to_numpy()

embedding_list = embeddings_df['ada_embedding'].to_numpy().flatten()
st.write(embeddings_df['ada_embedding'].shape, 'ada')
st.write(embedding_list.shape, 'list')

def get_embedding(text, model="text-embedding-ada-002"):
   return client.embeddings.create(input = [text], model=model).data[0].embedding


query = st.text_input("What topics are you interested in?")

# Search functionality
if query:
    # # Filter data based on query
    # filtered_data = text[text.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    # st.write(filtered_data)
    query_embedding = get_embedding(query, model='text-embedding-ada-002')
    query_embedding = query_embedding
    st.write(query_embedding.shape, 'query')
    

    # Calculate cosine similarity with each embedding in the list
    similarity_scores = [1 - cosine(query_embedding, emb) for emb in embeddings_df['ada_embedding']]

    st.write(similarity_scores)



############ UMAP ############

df = pd.read_csv('visual/umap_emb.csv')


# Create a basic chart
chart = alt.Chart(df).mark_point().encode(
    x=alt.X('x', axis=alt.Axis(title=None)),  # Replace 'x_column' with your actual x column name
    y=alt.Y('y', axis=alt.Axis(title=None)),   # Replace 'y_column' with your actual y column name
    tooltip=['title']
)

# Customize the chart to remove grid lines
chart = chart.configure_axis(
    grid=False,
    labels=False,
    ticks=False,
    domain=False
)

st.altair_chart(chart, use_container_width=True)