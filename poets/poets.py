import csv
import requests
import json
from bs4 import BeautifulSoup

# ----------------------------------------------------------------------------
# Scrape wiki pages and collect data

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

with open("poets.json", 'w') as outfile:
    json.dump(poets, outfile)

# ----------------------------------------------------------------------------
# Geocode data (lon/lat of birthplace and deathplace)

f = open("poets.json")
data = json.load(f)

for poet in data:
    if poet['birthplace'] != '':
        try:
            df = geocode(poet['birthplace'], provider="nominatim",
                         user_agent="pythongis_book", timeout=10)
            poet['birth_lon'] = df['geometry'][0].x
            poet['birth_lat'] = df['geometry'][0].y
        except:
            continue
    else:
        poet['birth_lon'] = 0
        poet['birth_lat'] = 0

    if poet['deathplace'] != '':
        try:
            df = geocode(poet['deathplace'], provider="nominatim",
                         user_agent="pythongis_book", timeout=10)
            poet['death_lon'] = df['geometry'][0].x
            poet['death_lat'] = df['geometry'][0].y
        except:
            continue
    else:
        poet['death_lon'] = 0
        poet['death_lat'] = 0

with open("poets.json.tmp", "w") as ofile:
    json.dump(data, ofile)

# ----------------------------------------------------------------------------
# Write to CSV


with open("poets.json.tmp") as infile:
    data = json.load(infile)

csv_file = open('poets.csv', 'w', newline='')
csv_writer = csv.writer(csv_file)

count = 0
for poet in data:
    if count == 0:
        header = poet.keys()
        csv_writer.writerow(header)
        count += 1
    csv_writer.writerow(poet.values())

csv_file.close()
