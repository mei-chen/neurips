from bs4 import BeautifulSoup
import re
from datetime import datetime
import json
import os

def clean_text(text):
    """Clean up text by removing extra whitespace and newlines"""
    if text:
        return ' '.join(text.strip().split())
    return None

def scrape_session_info(html_content):
    """
    Scrapes session information from the page header.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    session_info = {
        'session_name': None,
        'location': None,
        'time': None,
        'date': None
    }
    
    # Get session name
    title = soup.find('h2', class_='main-title')
    if title:
        session_info['session_name'] = clean_text(title.text)
    
    # Get location
    location = soup.find('h5', class_='text-center text-muted')
    if location:
        session_info['location'] = clean_text(location.text)
    
    # Find the time and date information
    header = soup.find('div', class_='card-header')
    if header:
        # Look for the text-center div that contains time info
        text_center = header.find('div', class_='text-center')
        if text_center:
            # Find all nested divs and look for one containing time info
            for div in text_center.find_all('div', recursive=False):
                text = clean_text(div.text)
                if text and 'CST' in text:
                    # Remove bookmark text
                    text = text.split('(Bookmark)')[0].strip()
                    
                    # Extract date and time using regex
                    match = re.match(r'(\w+ \d+ \w+) (\d+(?::\d+)? (?:a\.m\.|p\.m\.) CST) *(?:&mdash;|—) *(\d+(?::\d+)? (?:a\.m\.|p\.m\.) CST)', text)
                    if match:
                        session_info['date'] = match.group(1)
                        start_time = match.group(2).replace(' CST', '')
                        end_time = match.group(3).replace(' CST', '')
                        session_info['time'] = f"{start_time} - {end_time}"
                    break
    
    return session_info

def scrape_posters(html_content):
    """
    Scrapes poster and session information from NeurIPS HTML content.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    session_info = scrape_session_info(html_content)
    
    # Get poster information
    posters = []
    poster_cards = soup.find_all('div', class_='track-schedule-card')
    
    for card in poster_cards:
        poster_info = {
            'title': None,
            'abstract': None,
            'authors': None,
            'poster_number': None
        }
        
        # Get poster number
        poster_num_div = card.find('div', title='Poster Position')
        if poster_num_div:
            poster_info['poster_number'] = clean_text(poster_num_div.text.strip('#'))
        
        # Get title
        title_element = card.find('h5')
        if title_element and title_element.find('a'):
            poster_info['title'] = clean_text(title_element.find('a').text)
        
        # Get authors
        authors_element = card.find('p', class_='text-muted')
        if authors_element:
            poster_info['authors'] = clean_text(authors_element.text)
        
        # Get abstract
        abstract_div = card.find('div', class_='abstract')
        if abstract_div:
            poster_info['abstract'] = clean_text(abstract_div.text)
        
        posters.append(poster_info)
    
    return {
        'session_info': session_info,
        'posters': posters
    }

def main():
    all_sessions = []
    processed_files = 0
    
    # Process all HTML files in current directory
    for filename in os.listdir('.'):
        if filename.endswith('.html'):
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    html_content = file.read()
                
                session_data = scrape_posters(html_content)
                all_sessions.append(session_data)
                processed_files += 1
                
                # Print session information
                info = session_data['session_info']
                print(f"\nProcessed {filename}:")
                print(f"Session Name: {info['session_name']}")
                print(f"Location: {info['location']}")
                print(f"Date: {info['date']}")
                print(f"Time: {info['time']}")
                print(f"Found {len(session_data['posters'])} posters")
                
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
    
    # Save combined results
    if all_sessions:
        with open('all_sessions.json', 'w', encoding='utf-8') as f:
            json.dump(all_sessions, f, indent=2, ensure_ascii=False)
        print(f"\nSaved {len(all_sessions)} sessions to all_sessions.json")
    else:
        print("No sessions found in any files")

if __name__ == "__main__":
    main()