import os
from openai import OpenAI
import pandas as pd
import tiktoken
import os
from dotenv import load_dotenv

load_dotenv()
# Access your API key
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(
   api_key=OPENAI_API_KEY,
)

df = pd.read_csv('data/combined.csv')
df = df.rename(columns={'h5_strong_texts': 'title', 
                        'abstract_texts': 'abstract'})
df['abstract'] = df['abstract'].str[1:]
# df['combined'] = "Title: " + df['title'] + "\nAbstract: " + df['abstract']
df['combined'] = df['title'] + "\n" + df['abstract']
print(df['combined'][0])

# df['combined'] = "Title: " + df[0] + " Abstract:" + df[1][2:]
# print(df['combined'])

# # Function to get embeddings
# def get_embeddings(texts):
#     response = openai.Embedding.create(
#         input=texts,
#         model="text-similarity-babbage-001"  # or choose another suitable model
#     )
#     return [embedding['embedding'] for embedding in response['data']]


def get_embedding(text, model="text-embedding-ada-002"):
   return client.embeddings.create(input = [text], model=model).data[0].embedding

df['ada_embedding'] = df['combined'].apply(lambda x: get_embedding(x, model='text-embedding-ada-002'))
df.to_csv('embedding/embedded_combined1.csv', index=False)

