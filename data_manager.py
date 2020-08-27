import paho.mqtt.client as mqtt
# from time import sleep
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
    result = db.search(query[type] == value)
    if(len(str(result))) < 5:
        return None
    return result

def search_greater(type, value):
    result = db.search(query[type] > value)
    if(len(str(result))) < 5:
        return None
    return result

def search_lower(type, value):
    result = db.search(query[type] < value)
    if(len(str(result))) < 5:
        return None
    return result

def search_in_range(type, lower, higher):
    result = db.search((lower <= query[type]) & (query[type] <= higher))
    if(len(str(result))) < 5:
        return None
    return result

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("I manage to connect to server")
    else:
        print("Something went wrong with connecting, rc = ", rc)

def on_log(client, userdata, level, buf):
    print("Log: ", buf)

def get_result(decoded):
    # status_file = open("status.txt","w")
    # status_file.write("filling")
    # status_file.close()

    lower = decoded[0:10]
    higher = decoded[11:21]
    print(f"lower: {lower}, higher: {higher}")
    result = search_in_range("date",lower,higher)
    return result

def status_finished():
    brooker = "127.0.0.1"
    client = mqtt.Client("Status_changer")

    client.on_log = on_log
    client.on_connect = on_connect

    client.connect(brooker)
    client.loop_stop()
    client.publish("request_status", "done")
    client.loop_stop()
    # status_file = open("status.txt","w")
    # status_file.write("ready")
    # status_file.close()
    print("data ready")

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

    if msg.topic == 'gui_request/rain':
        result = get_result(decoded)
        
        result_file = open("result_file.csv","w")
        for row in result:
            result_file.write(+row["date"]+','+str(row["rain"])+"\n")
        result_file.close()

        status_finished()

    if msg.topic == 'gui_request/temp':
        result = get_result(decoded)

        result_file = open("result_file.csv","w")
        for row in result:
            result_file.write(row["date"]+','+str(row["temp"])+"\n")
        result_file.close()

        status_finished()

    if msg.topic == 'gui_request/press':
        result = get_result(decoded)

        result_file = open("result_file.csv","w")
        for row in result:
            result_file.write(row["date"]+','+str(row["press"])+"\n")
        result_file.close()

        status_finished()

    if msg.topic == 'gui_request/wind':
        result = get_result(decoded)

        result_file = open("result_file.csv","w")
        for row in result:
            result_file.write(row["date"]+','+str(row["wind"])+"\n")
        result_file.close()

        status_finished()

        # client.publish("data",result)
    
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
    if not (dataType == "fillDatabase"):
        client.subscribe(f"gui_request/{dataType}")

client.subscribe("requestdata")

try:
    while True:
        client.loop_start()
finally:
    client.loop_stop()
