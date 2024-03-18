import csv
import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # Updated import
from bs4 import BeautifulSoup

def search_keywords(keywords, domain):
    options = Options()
    options.add_argument("--headless")  # Run Chrome in headless mode (without opening browser window)

    # Get the Chrome driver path
    driver_path = ChromeDriverManager().install()

    driver = webdriver.Chrome(options=options, executable_path=driver_path)
    
    results = []
    for keyword in keywords:
        url = f"https://www.google.co.in/search?q={'+'.join(keyword.split())}&num=60&gl=in&hl=en"
        driver.get(url)
        time.sleep(2)  # Allowing time for the page to load
        html_content = driver.page_source
        position = find_domain_ranking(html_content, domain)
        results.append({'Keyword': keyword, 'Position': position})

    driver.quit()
    return results

def find_domain_ranking(html_content, domain):
    soup = BeautifulSoup(html_content, 'html.parser')
    results = soup.find_all('div', class_='yuRUbf')

    for i, result in enumerate(results, 1):
        link = result.find('a')['href']
        if domain in link:
            return i
    return None

def main():
    st.title("Google SERP Position Finder")

    # Input box for entering keywords
    keywords_input = st.text_area("Enter keywords (one per line):")
    keywords = [keyword.strip() for keyword in keywords_input.split('\n') if keyword.strip()]

    domain = st.text_input("Enter domain to search for:", "mygreatlearning.com")

    if st.button("Search"):
        if not keywords:
            st.warning("Please enter at least one keyword.")
        else:
            st.info("Searching Google for each keyword...")
            results = search_keywords(keywords, domain)

            # Display results in a table
            st.table(results)

            # Save results to CSV file
            output_file = 'SERP_Positions.csv'
            with open(output_file, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['Keyword', 'Position'])
                writer.writeheader()
                writer.writerows(results)

            st.success(f"Data saved to {output_file}")

if __name__ == "__main__":
    main()
