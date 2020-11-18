from django.test import TestCase

# Create your tests here.


import pandas as pd



def setCoorinates():
    file = pd.read_csv('getData/coordonateTari.csv')
    for i in file.values:
        name, lat, long = i[0], i[1], i[2]
        #c = County(name, lat, long)
        # try:
        #     c.save()
        # except():
        #     # if the're a problem anywhere, you wanna know about it
        #     print("there was a problem with line")


setCoorinates()
