import requests
import pandas as pd
from bs4 import BeautifulSoup

# how often are rows added and how do we know?
url_to_scrape = 'https://mvlwb.com/registry/'

div_class_to_extract = 'view-content'
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

url = 'https://mvlwb.com/registry/W2009C0003'

#swagger

def scrape_links_in_div(url, div_class):
    try:
        # Make a request to the URL and get the HTML content
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div with the specified class
        div_element = soup.find('div', class_=div_class)

        if div_element:
            links = div_element.find_all('a', href=True)
            for x2 in links:
                title.append(x2.getText())

            for x3 in div_element.select('td[class*="received"]'):
                received.append(x3.getText())

            for x4 in div_element.select('td[class*="uploaded"]'):
                uploaded.append(x4.getText())

            link = [link2['href'] for link2 in links]

            n=3
            for i in link:
                file_ext.append(i[-n:])

        else:
            print(f"No div with class '{div_class}' found on the webpage {url}.")

    except requests.RequestException as e:
        print(f"Failed to retrieve the webpage {url}. Error: {e}")


# List of URLs to scrape
list_of_urls = permits[0:1]

for url in list_of_urls:
    scrape_links_in_div(url, div_class_to_extract)

columns = [title, file_ext, received, uploaded, link]
it = iter(columns)
the_len = len(next(it))

for j in columns:
    print(len(j))

if all(len(l) == the_len for l in it):
    print('lists have same length!')
else:
    print('not all lists have same length!')
    exit()


df = pd.DataFrame({'title': title, 'file_ext': file_ext, 'received': received,
                      'uploaded': uploaded, 'link': link})
df.to_excel("test1.xlsx", sheet_name="TheSauce", index=False)













