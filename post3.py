import csv
import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager, ChromeType
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException

def search_keyword(keyword, domain, country_code, driver):
    results = []
    try:
        url = f"https://www.google.com/search?q={'+'.join(keyword.split())}&num=60&gl={country_code}&hl=en"
        driver.get(url)
        time.sleep(2)  # Allowing time for the page to load
        html_content = driver.page_source
        position, urls = find_domain_ranking(html_content, domain)
        results.append({'Keyword': keyword, 'Position': position, 'URLs': '\n'.join(urls)})
    except WebDriverException as e:
        st.error(f"An error occurred for keyword '{keyword}': {e}")
    
    return results

def find_domain_ranking(html_content, domain):
    soup = BeautifulSoup(html_content, 'html.parser')
    results = soup.find_all('div', class_='yuRUbf')
    urls = []

    for i, result in enumerate(results, 1):
        link = result.find('a')['href']
        if domain in link:
            urls.append(link)
            return i, urls
        urls.append(link)
    return None, urls

def main():
    st.title("Google SERP Position Finder")

    # Input box for entering keywords
    keywords_input = st.text_area("Enter keywords (one per line):")
    keywords = [keyword.strip() for keyword in keywords_input.split('\n') if keyword.strip()]

    domain = st.text_input("Enter domain to search for:", "mygreatlearning.com")

    country_code = st.selectbox("Select Country Code:", ["US", "UK", "India"])

    country_code_map = {"US": "us", "UK": "uk", "India": "in"}

    if st.button("Search"):
        if not keywords:
            st.warning("Please enter at least one keyword.")
        else:
            st.info("Searching Google for each keyword...")
            options = Options()
            options.add_argument("--headless")  # Run Chrome in headless mode (without opening browser window)
            driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            service = webdriver.chrome.service.Service(driver_path)
            driver = webdriver.Chrome(service=service, options=options)
            all_results = []
            try:
                for keyword in keywords:
                    results = search_keyword(keyword, domain, country_code_map[country_code], driver)
                    all_results.extend(results)
            finally:
                driver.quit()

            if all_results:
                # Display results in a table
                st.table(all_results)

                # Save results to CSV file
                output_file = 'SERP_Positions.csv'
                with open(output_file, 'w', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=['Keyword', 'Position', 'URLs'])
                    writer.writeheader()
                    writer.writerows(all_results)

                st.success(f"Data saved to {output_file}")

if __name__ == "__main__":
    main()
