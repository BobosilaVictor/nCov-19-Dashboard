import pandas as pd
import csv

data = pd.read_csv("coordonate.txt")
tari = data.iloc[:,1]
x = data.iloc[:, -2]
y = data.iloc[:, -1]
with open('coordonateTari.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ["judet","lat", "long"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(x.values)):
        writer.writerow({fieldnames[0]: tari.values[i], fieldnames[1]: x.values[i], fieldnames[2]: y.values[i]})
