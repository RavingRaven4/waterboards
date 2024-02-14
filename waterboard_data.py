from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

# options = Options()
    # options.add_argument("--headless")

url_to_scrape = 'https://mvlwb.com/registry/'
div_class = 'view-content'
wek_permits = pd.read_excel('wk_data22.xlsx')
file_nums = pd.DataFrame(wek_permits['File Number'])

permits = []

for i in range(len(file_nums)):
    permits.append(str(f"{url_to_scrape}{file_nums['File Number'][i]}"))

permit = []
title = []
file_ext = []
received = []
uploaded = []
link = []

k = 'https://mvlwb.com/registry/mv2001l2-0008'

# for k in permits:
response = requests.get(k)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')
div_element = soup.find('div', class_=div_class)
if div_element:
    links = div_element.find_all('a', href=True)
    for x1 in range(len(links)):
        permit.append(k.split('y/', 1)[1])
    for x2 in links:
        title.append(x2.getText())
    for x3 in div_element.select('td[class*="received"]'):
        received.append(x3.getText())
    for x4 in div_element.select('td[class*="uploaded"]'):
        uploaded.append(x4.getText())
    for x5 in range(len(links)):
        link.append(links[x5]['href'])
        file_ext.append(link[-1].split('.')[-1])
    if len(links) > 90:
        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 7)
        driver.get(k + '?page=1')
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # time.sleep(4)
        # next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[title="Go to next page"]')))
        # driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
        # next_button.click()
        html = driver.page_source
        soup2 = BeautifulSoup(html, 'html.parser')
        div_element2 = soup2.find('div', class_=div_class)
        links2 = div_element2.find_all('a', href=True)
        for x1_1 in range(len(links2)):
            permit.append(k.split('y/', 1)[1])
        for x2_1 in links2:
            title.append(x2_1.getText())
        for x3_1 in div_element2.select('td[class*="received"]'):
            received.append(x3_1.getText())
        for x4_1 in div_element2.select('td[class*="uploaded"]'):
            uploaded.append(x4_1.getText())
        for x5_1 in range(len(links2)):
            link.append(links2[x5_1]['href'])
            file_ext.append(link[-1].split('.')[-1])



columns = [permit, title, file_ext, received, uploaded, link]
for j in columns:
    print(len(j))

it = iter(columns)
the_len = len(next(it))
if all(len(l) == the_len for l in it):
    print('lists have same length!')
else:
    print('not all lists have same length!')
    exit()

df = pd.DataFrame({'permit': permit, 'title': title, 'file_ext': file_ext, 'received': received,
                      'uploaded': uploaded, 'link': link})
df.to_excel("test1.xlsx", sheet_name="TheSauce", index=False)













