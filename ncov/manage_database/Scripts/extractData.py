import unidecode
import bs4 as bs
from urllib.request import Request, urlopen
import csv
import pandas as pd
import datetime


def extractDataFromSite(pathCoordinates, pathSite, date):
    try:
        req = Request(pathSite, headers={'User-Agent': 'Mozilla/5.0'})
        source = urlopen(req).read()
        soup = bs.BeautifulSoup(source, 'html.parser')

        c = soup.find('table')
        head = c.find('tr')
        head = head.find_all('td')
        h = []
        # get the header and remove diacritics
        for i in head[1:]:
            text = unidecode.unidecode(i.text)
            h.append(text)
        h.append("Date")
        # print(h)
        table = {}
        # get the data from table and remove diacritics
        for tr in c.find_all('tr')[1:-2]:
            tr_list = []
            for td in tr.find_all('td'):
                text_td = unidecode.unidecode(td.text)
                tr_list.append(text_td)
            tr_list.append(date)
            # Create dictionary with the country name as the key and nr of deaths etc.. as values
            table[tr_list[1]] = tr_list[2:]
        return h, table
    except FileNotFoundError:
        print("Need coordinates")


# write in csv
def createCsv(path, header, table):
    with open(path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = header
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        try:
            for row in table:
                writer.writerow(
                    {fieldnames[0]: row, fieldnames[1]: table[row][0], fieldnames[2]: table[row][1],
                     fieldnames[3]: table[row][2], fieldnames[4]: table[row][3]})
        except IndexError:
            print("Not enough countries")


# Use to get data from the day before

current_date = datetime.datetime.today().strftime('%d-%m-%Y')
nr = int(current_date[:2]) - 1
current_date = str(nr) + current_date[2:]
path = 'http://www.ms.ro/2020/11/24/buletin-informativ-' + current_date + '/'
header, table = extractDataFromSite('coordonateTari.csv', path, current_date)
createCsv(current_date + '.csv', header, table)


def main():
    try:
        current_date = datetime.datetime.today().strftime('%d-%m-%Y')
        path = 'http://www.ms.ro/2020/11/24/buletin-informativ-' + current_date + '/'
        # Give path to the csv containing the coordinates, link of the website
        # returns the header and the data inside the table
        header, table = extractDataFromSite('coordonateTari.csv', path, current_date)
        createCsv(current_date + '.csv', header, table)

    except:
        print("Data for today was not yet uploaded")
