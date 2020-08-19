import paho.mqtt.client as mqtt
import time
from tinydb import TinyDB, Query
import json
import ast
import csv

db = TinyDB('db.json')
query = Query()

# TODO:
# def aggregate_day_average(target):
#     nothingForNow = 0
#     return nothingForNow

def sth():
    with open('2020_synop_csv/s_d_t_01_2020.csv', newline='') as csvfile:
        fieldNames = ['number','city','year','month','day','cloud','NOS','wind','FWS','temp','TEMP','pressW','CPW','moisture','WLGS','press','PPPS','pressSea','PPPM','rainDay','WODZ','rainNight','WONO']
        sdtreader = csv.DictReader(csvfile,fieldnames=fieldNames)
        for row in sdtreader:
            print(row['number'], row['wind'], row['press'])
            word = row['press']
            print(type(word),type(row))

def search_equal(type, value):
    result = str(db.search(query[type] == value))
    if(len(result)) < 5:
        return ""
    return result

def search_greater(type, value):
    result = str(db.search(query[type] > value))
    if(len(result)) < 5:
        return ""
    return result

def search_lower(type, value):
    result = str(db.search(query[type] < value))
    if(len(result)) < 5:
        return ""
    return result

def search_in_range(type, lower, higher):
    result = str(db.search((lower <= query[type]) & (query[type] <= higher)))
    if(len(result)) < 5:
        return ""
    return result

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("I manage to connect to server")
    else:
        print("Something went wrong with connecting, rc = ", rc)
def on_log(client, userdata, level, buf):
    print("Log: ", buf)

def on_messege(client, userdata, msg):
    decoded = msg.payload.decode("utf-8")
    print(f"Message I received -> Topic: {msg.topic}, Message: {decoded}")

    if msg.topic == 'krakow/fillDatabase':
        newDict = ast.literal_eval(decoded)
        print(newDict)
        if not db.contains((query.date == newDict.get("date")) & (query.hour == newDict.get("hour"))):
            db.insert(newDict)
            print("Inserted")
        else:
            print("Already exists")

    if msg.topic == '': # nazwa publishera (operator?)
        lower = decoded[0:10]
        higher = decoded[11:21]
        result = search_in_range("date",lower,higher)
        print(result)
        client.publish("data",result)
    
    # if msg.topic[0:10] == 'visualizer':
    #     if msg.topic[11:15] == 'day':
    #         day = decoded
    #         print(day)

    #     elif msg.topic[11:16] == 'week':
    #         lower = decoded[0:10]
    #         higher = decoded[11:21]
    #         result = search_in_range("date",lower,higher)
    #         print(result)
            
    #     elif msg.topic[11:17] == 'month':
    #         lower = decoded[0:10]
    #         higher = decoded[11:21]
    #         result = search_in_range("date",lower,higher)
    #         print(result)

    #     elif msg.topic[11:16] == 'year':
    #         lower = decoded[0:10]
    #         higher = decoded[11:21]
    #         result = search_in_range("date",lower,higher)
    #         print(result)

brooker = "127.0.0.1"
client = mqtt.Client("data_manager")

client.on_connect = on_connect
client.on_log = on_log
client.on_message = on_messege

subTypes = ["temp", "wind", "press", "rain", "fillDatabase"]

timePeriods = ["day", "week", "month", "year"]

client.connect(brooker)

for dataType in subTypes:
    client.subscribe(f"krakow/{dataType}")

client.subscribe("requestdata")

try:
    while True:
        client.loop_start()
finally:
    client.loop_stop()
