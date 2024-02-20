import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

url_to_scrape = 'https://mvlwb.com/registry/'
div_class = 'view-content'

# check this
wek_permits = pd.read_excel('wekeezhii_data_15_02_2024.xlsx')
file_nums = pd.DataFrame(wek_permits['file_number'])

permits = []
for i in range(len(file_nums)):
    permits.append(str(f"{url_to_scrape}{file_nums['file_number'][i]}"))


permit = []
title = []
file_ext = []
received = []
uploaded = []
link = []

# k1 = 'https://mvlwb.com/registry/w2020l2-0004'
# k2 = 'https://mvlwb.com/registry/W2015C0002'
# k3 = 'https://mvlwb.com/registry/mv2001l8-0001'
# k4 = 'https://mvlwb.com/registry/w2012l2-0001'
#
# permits2 = []
# permits2 += [k1, k2, k3, k4]

for k in permits:
    stew = []
    i = 0
    while True:
        response = requests.get(k + '?page=' + str(i))
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        div_element = soup.find('div', class_=div_class)
        if div_element == None and i == 0:
            print(k + ': empty permit')
            break
        if div_element == None:
            break
        elif not stew:
            pass
        elif div_element == stew[-1]:
            print(k + ': multi-pager (' + str(i) + ')')
            break

        stew.append(div_element)
        i += 1

    for potato in stew:
        if not stew:
            break
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

        print(k + ':  ' + str(len(links)))


columns = [permit, title, file_ext, received, uploaded, link]
for j in columns:
    print(len(j))


df = pd.DataFrame({'permit': permit, 'file_ext': file_ext, 'received': received,
                      'uploaded': uploaded, 'title': title, 'link': link})

# df['date'] = df['date'].apply(lambda x: datetime.strptime(x, '%d'))

df.to_excel("wek_file_types_" + datetime.now().strftime("%d_%m_%Y") + '_test.xlsx', sheet_name="TheSauce", index=False)













