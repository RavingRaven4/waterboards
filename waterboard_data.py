import requests
import pandas as pd
from bs4 import BeautifulSoup

url_to_scrape = 'https://mvlwb.com/registry/'
div_class = 'view-content'

# check this
wek_permits = pd.read_excel('wekeezhii_data_15_02_2024.xlsx')
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


for k in permits:
    stew = []
    i = 0
    while True:
        response = requests.get(k + '?page=' + str(i))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        div_element = soup.find('div', class_=div_class)
        if div_element == None:
            break
        stew.append(div_element)
        i += 1

    for potato in stew:
        links = potato.find_all('a', href=True)
        for x1 in range(len(links)):
            permit.append(k.split('y/', 1)[1])
        for x2 in links:
            title.append(x2.getText())
        for x3 in potato.select('td[class*="received"]'):
            received.append(x3.getText())
        for x4 in potato.select('td[class*="uploaded"]'):
            uploaded.append(x4.getText())
        for x5 in range(len(links)):
            link.append(links[x5]['href'])
            file_ext.append(link[-1].split('.')[-1])


columns = [permit, title, file_ext, received, uploaded, link]
for j in columns:
    print(len(j))

df = pd.DataFrame({'permit': permit, 'title': title, 'file_ext': file_ext, 'received': received,
                      'uploaded': uploaded, 'link': link})
df.to_excel("test2.xlsx", sheet_name="TheSauce", index=False)













