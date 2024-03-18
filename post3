import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import base64
import time
import datetime
import os

# Define keywords
KEYWORDS = [
    "keyword1",
    "keyword2",
    # Add more keywords as needed
]

def get_search_results(keyword):
    url = f"https://www.google.co.in/search?q={'+'.join(keyword.split())}&num=60&gl=in&hl=en"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107 Safari/537",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        st.error(f"Failed to retrieve search results. Status code: {response.status_code}")
        return None

def find_domain_ranking(html_content, domain):
    soup = BeautifulSoup(html_content, 'html.parser')
    results = soup.find_all('div', class_='yuRUbf')
    urls_ranking = []
    for i, result in enumerate(results, start=1):
        url = result.find('a')['href']
        urls_ranking.append(url)
        if domain.lower() in result.get_text().lower():
            return i, urls_ranking
    return None, urls_ranking

def clean_domain(domain):
    domain = domain.lower()
    if domain.startswith('http://') or domain.startswith('https://'):
        domain = domain.split("//")[-1]
    if domain.startswith('www.'):
        domain = domain.split("www.")[-1]
    return domain

def process_keywords():
    data = []
    for keyword in KEYWORDS:
        st.info(f"Processing keyword: {keyword}")
        search_results = get_search_results(keyword)
        if search_results:
            ranking, urls_ranking = find_domain_ranking(search_results, clean_domain(domain))
            if ranking:
                urls_ranking_str = "\n".join(urls_ranking)
                data.append([keyword, ranking, urls_ranking_str])
            else:
                urls_ranking_str = "\n".join(urls_ranking)
                data.append([keyword, "Not Found", urls_ranking_str])
        else:
            data.append([keyword, "Failed", ""])

        # Wait for one minute before processing the next keyword
        time.sleep(60)

    # Store the processed data in a CSV file
    filename = f"data_{datetime.date.today()}.csv"
    df = pd.DataFrame(data, columns=["Keyword", "Ranking", "URLs Ranking"])
    df.to_csv(filename, index=False)

    return df

def clear_processed_data():
    # Delete all CSV files in the current directory
    for file in os.listdir():
        if file.endswith(".csv") and file.startswith("data_"):
            os.remove(file)

def main():
    st.title("Google Domain Ranking Checker")

    # Process keywords and display results
    processed_data = process_keywords()
    st.table(processed_data)

    # Download button
    if st.button("Download Position Data"):
        filename = f"data_{datetime.date.today()}.csv"
        with open(filename, "rb") as file:
            b64 = base64.b64encode(file.read()).decode()
            href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download CSV</a>'
            st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    # Clear processed data at midnight
    while True:
        current_time = datetime.datetime.now().time()
        if current_time.hour == 0 and current_time.minute == 0:
            clear_processed_data()
            break

        time.sleep(60)

    main()
