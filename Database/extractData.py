import unidecode
import bs4 as bs
from urllib.request import Request, urlopen
import csv
import pandas as pd


def extractDataFromSite(pathCoordinates):
    try:
        req = Request('http://www.ms.ro/category/stiri/', headers={'User-Agent': 'Mozilla/5.0'})
        source = urlopen(req).read()
        soup = bs.BeautifulSoup(source, 'html.parser')
        c = soup.find('table')
        head = c.find('tr')
        head = head.find_all('td')
        h = []
        # get the header
        for i in head:
            text = unidecode.unidecode(i.text)
            h.append(text)

        # print(h)
        table = {}
        # get the data from table
        for tr in c.find_all('tr')[1:-2]:
            tr_list = []
            for td in tr.find_all('td'):
                text_td = unidecode.unidecode(td.text)
                tr_list.append(text_td)
            table[tr_list[1]] = tr_list[2:]

        coordinates = pd.read_csv(pathCoordinates)
        h.append(coordinates.columns[-2])
        h.append(coordinates.columns[-1])

        # print(h)
        for (judet, lat, long) in coordinates.values:
            if judet in table:
                # print('got you')
                table[judet].append(lat)
                table[judet].append(long)
        return h, table
    except FileNotFoundError:
        print("Need coordinates")


# write in csv
def createCsv(path, header, table):
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        i = 1
        try:
            for row in table:
                writer.writerow(
                    {fieldnames[0]: i, fieldnames[1]: row, fieldnames[2]: table[row][0], fieldnames[3]: table[row][1],
                     fieldnames[4]: table[row][2], fieldnames[5]: table[row][3], fieldnames[6]: table[row][4]})
                i = i + 1

        except IndexError:
            print("Not enough coutries")


# TO DO
# GET DATE
def extractDate():
    pass


header, table = extractDataFromSite('coordonateTari.csv')
createCsv('numeDoc1.csv', header, table)