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

k = 'https://mvlwb.com/registry/w2014l3-0002'

# for k in permits:
response = requests.get(k)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')
div_element = soup.find_all("div", {"class": "view-content"})

if soup.find_all("div", {"class": "view-content"}):
    print("Tag Found")
else:
    print("Not found")

stew = []
i = 0
while True:
    response = requests.get(k + '?page=' + str(i))
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    div_element = soup.find('div', class_=div_class)
    if div_element == None:
        break
    # div_element = soup.find_all("div", {"class": "view-content"})
    stew.append(div_element)
    i += 1

len(stew)





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
df.to_excel("test2.xlsx", sheet_name="TheSauce", index=False)













