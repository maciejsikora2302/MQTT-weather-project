import time
from tinydb import TinyDB, Query
import json
import ast
import csv

db = TinyDB('db.json')
query = Query()

def fill(filename):
    with open('2020_synop_csv/'+filename, newline='') as csvfile:
        fieldNames = ['number','city','year','month','day','cloud','NOS','wind','FWS','temp','TEMP','pressW','CPW','moisture','WLGS','press','PPPS','pressSea','PPPM','rainDay','WODZ','rainNight','WONO']
        sdtreader = csv.DictReader(csvfile,fieldnames=fieldNames)
        for row in sdtreader:
            if(row['number'] == '350190566'):
                newDict = dict ([
                    ("date",row['year']+'-'+row['month']+'-'+row['day']),
                    ("hour",8),
                    ("temp",row['temp']),
                    ("wind",float(row['wind'])),
                    ("press",float(row['press'])),
                    ("rain",float(row['rainDay'])+float(row['rainNight']))
                ])
                if not db.contains((query.date == newDict.get("date")) & (query.hour == newDict.get("hour"))):
                    db.insert(newDict)

filenames = ['s_d_t_01_2020.csv','s_d_t_02_2020.csv','s_d_t_03_2020.csv','s_d_t_04_2020.csv','s_d_t_05_2020.csv','s_d_t_06_2020.csv','s_d_t_07_2020.csv']

# for filename in filenames:
#     fill(filename)