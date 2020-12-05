from urllib.error import HTTPError

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


def main():
    try:
        x = datetime.datetime.now()
        d = x.strftime("%d-%m-%Y")
        # http://www.ms.ro/2020/12/04/buletin-informativ-04-12-2020/
        path = 'http://www.ms.ro/' + x.strftime('%Y/%m/%d') + '/buletin-informativ-' + d + '/'
        print(path)
        header, table = extractDataFromSite('coordonateTari.csv', path, d)
        createCsv(x.strftime('%d-%m-%Y') + '.csv', header, table)
    except HTTPError:
        print("Data for today was not yet uploaded")
        x = datetime.datetime.now()
        yesterday = x.strftime("%d")
        yesterday = str(int(yesterday) - 1)
        if int(yesterday) < 10 :
            yesterday = '0' + yesterday
        d = yesterday + x.strftime("-%m-%Y")
        # http://www.ms.ro/2020/12/04/buletin-informativ-04-12-2020/
        path = 'http://www.ms.ro/' + x.strftime('%Y/%m/') + yesterday + '/buletin-informativ-' + yesterday + x.strftime(
            "-%m-%Y") + '/'
        print(path)
        header, table = extractDataFromSite('coordonateTari.csv', path, d)
        createCsv(yesterday + x.strftime('-%m-%Y') + '.csv', header, table)


main()
