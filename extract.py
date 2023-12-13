import csv
from bs4 import BeautifulSoup
# import requests

HTML_NAME = 'sesh6.html'
CSV_NAME = 'sesh6.csv'

# Function to extract text from HTML
def extract_text_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Extracting text from <h5><strong></strong></h5>
    h5_strong_texts = [tag.get_text() for tag in soup.find_all('h5') if tag.strong]

    # Extracting text from <div class="abstract"></div>
    abstract_texts = [div.get_text() for div in soup.find_all('div', class_='abstract')]

    return h5_strong_texts, abstract_texts


# Read HTML content from file
with open(HTML_NAME, 'r', encoding='utf-8') as file:
    html_content = file.read()

h5_strong_texts, abstract_texts = extract_text_from_html(html_content)

# print("Texts in <h5><strong>:</strong></h5>")
# for text in h5_strong_texts:
#     print(text)

# print("\nTexts in <div class='abstract'>:")
# for text in abstract_texts:
#     print(text)

# write data to csv

with open(CSV_NAME, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['h5_strong_texts', 'abstract_texts'])
    writer.writerows(zip(h5_strong_texts, abstract_texts))