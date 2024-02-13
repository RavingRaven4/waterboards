from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time



# ELIMINATE HEADERS


def scrape_table_with_hidden(url):
    # options = Options()
    # options.add_argument("--headless")
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 7)

    driver.get(url)

    all_data = []

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        table = soup.find('table', {'class': 'table table-striped cols-5'})

        if table:
            for row in table.find_all('tr'):
                columns = [col.text.strip() for col in row.find_all(['th', 'td'])]
                all_data.append(columns)

        try:
            next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[title="Go to next page"]')))
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(4)
            next_button.click()
        except TimeoutException:
            break

    driver.quit()
    return all_data

def save_to_xlsx(data, filename='wk_data22.xlsx'):
    df = pd.DataFrame(data[1:], columns=data[0])  # Assuming the first row contains headers
    df.to_excel(filename, index=False)

url = 'https://wlwb.ca/registry?f%5B0%5D=region%3AWek%27%C3%A8ezh%C3%ACi'
table_data = scrape_table_with_hidden(url)

if table_data:
    save_to_xlsx(table_data, filename='wk_data22.xlsx')
    print("Data has been saved to wk_data22.xlsx.")
else:
    print("No data to save.")