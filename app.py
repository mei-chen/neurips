import streamlit as st
import pandas as pd
import altair as alt
import csv

st.set_page_config(layout="wide")


st.title("NeurIPS Poster Search")

# Load your CSV file
text = pd.read_csv('visual/combined.csv')


query = st.text_input("What poster topics are you looking for?")


# Search functionality
if query:
    # Filter data based on query
    filtered_data = text[text.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)]
    st.write(filtered_data)



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