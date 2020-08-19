import csv

def getData(fileName):
    with open(fileName, newline='') as csvfile:
        sdtreader = csv.reader(csvfile, delimiter=' ')
        for row in sdtreader:
            print(', '.join(row))

    with open('2020_synop_csv/s_d_t_01_2020.csv', newline='') as csvfile:
        fieldNames = ['number','city','year','month','day','cloud','NOS','wind','FWS','temp','TEMP','pressW','CPW','moisture','WLGS','press','PPPS','pressSea','PPPM','rainDay','WODZ','rainNight','WONO']
        sdtreader = csv.DictReader(csvfile,fieldnames=fieldNames)
        for row in sdtreader:
            print(row['number'], row['wind'], row['press'])
            word = row['press']
            print(type(word),type(row))