import requests
import json
from bs4 import BeautifulSoup

url1 = "https://en.wikipedia.org/wiki/List_of_poets_from_the_United_States"
poets = []

page = requests.get(url1)
soup = BeautifulSoup(page.content, 'html.parser')
object = soup.find(id="mw-content-text")
items = object.find_all(class_="div-col")

for tag in items:
    for row in tag.findAll('a'):
        poet = {}
        poet['href'] = 'https://en.wikipedia.org' + row['href']

        poet['name'] = row['title']
        if poet['name'][0].isnumeric():
            continue

        poets.append(poet)

foo = []

for poet in poets:
    url2 = poet['href']
    page = requests.get(url2)
    soup = BeautifulSoup(page.text, 'html.parser')

    try:
        first_div = soup.find('div', {'class': 'birthplace'})
        first_a = first_div.find('a')
        birthplace = first_a['title']

        poet['birthplace'] = birthplace
        print('birthplace: ', birthplace)
    except:
        poet['birthplace'] = ""
        pass

    try:
        first_div = soup.find('div', {'class': 'deathplace'})
        first_a = first_div.find('a')
        deathplace = first_a['title']

        poet['deathplace'] = deathplace
        print("deathplace: ", deathplace)
    except:
        poet['deathplace'] = ""
        pass

    foo.append(poet)


with open("poets.json", 'w') as outfile:
    json.dump(foo, outfile)
