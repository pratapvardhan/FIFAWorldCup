import os
import hashlib
import requests
from bs4 import BeautifulSoup
import pandas as pd

if not os.path.exists('.cache'):
    os.makedirs('.cache')

ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36'
session = requests.Session()

def get(url):
    '''Return cached lxml tree for url'''
    path = os.path.join('.cache', hashlib.md5(url).hexdigest() + '.html')
    if not os.path.exists(path):
        print url
        response = session.get(url, headers={'User-Agent': ua})
        with open(path, 'w') as fd:
            fd.write(response.text.encode('utf-8'))
    return BeautifulSoup(open(path), 'html.parser')

def squads(url):
    result = []
    soup = get(url)
    year = url[29:33]
    for table in soup.find_all('table','sortable'):
        if "wikitable" not in table['class']:
            country = table.find_previous("span","mw-headline").text
            for tr in table.find_all('tr')[1:]:
                cells = [td.text.strip() for td in tr.find_all('td')]
                cells += [country, td.a.get('title') if td.a else 'none', year]
                result.append(cells)
    return result

years = range(1930,1939,4) + range(1950,2015,4)
result = []
for year in years:
    url = "http://en.wikipedia.org/wiki/"+str(year)+"_FIFA_World_Cup_squads"
    result += squads(url)

pd.DataFrame(result).to_csv('data.csv', index=False, encoding='utf-8')
