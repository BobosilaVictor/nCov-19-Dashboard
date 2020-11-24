import unidecode
import bs4 as bs
from urllib.request import Request, urlopen
import csv
import pandas as pd


def extractDataFromSite(pathCoordinates, pathSite):
    try:
        req = Request(pathSite, headers={'User-Agent': 'Mozilla/5.0'})
        source = urlopen(req).read()
        soup = bs.BeautifulSoup(source, 'html.parser')
        c = soup.find('table')
        head = c.find('tr')
        head = head.find_all('td')
        h = []
        # get the header and remove diacritics
        for i in head:
            text = unidecode.unidecode(i.text)
            h.append(text)

        # print(h)
        table = {}
        # get the data from table and remove diacritics
        for tr in c.find_all('tr')[1:-2]:
            tr_list = []
            for td in tr.find_all('td'):
                text_td = unidecode.unidecode(td.text)
                tr_list.append(text_td)
            # Create dictionary with the country name as the key and nr of deaths etc.. as values
            table[tr_list[1]] = tr_list[2:]

        coordinates = pd.read_csv(pathCoordinates)
        h.append(coordinates.columns[-2])
        h.append(coordinates.columns[-1])
        # Add the coordinates for every country
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
            print("Not enough countries")


# TO DO
# GET DATE
def extractDate():
    pass


# Give path to the csv containing the coordinates, link of the website
# returns the header and the data inside the table
header, table = extractDataFromSite('coordonateTari.csv', 'http://www.ms.ro/category/stiri/')
createCsv('numeDoc2.csv', header, table)
