import paho.mqtt.client as mqtt
# from time import sleep
from tinydb import TinyDB, Query
import json
import ast
import csv

db = TinyDB('db.json')
query = Query()

def search_in_range(type, lower, higher):
    result = db.search((lower <= query[type]) & (query[type] <= higher))
    # if len(str(result)) < 5:
    #     return None
    return result

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("I manage to connect to server")
    else:
        print("Something went wrong with connecting, rc = ", rc)

def on_log(client, userdata, level, buf):
    print("Log: ", buf)

def get_result(lower,higher):
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
        lower = decoded[0:10]
        higher = decoded[11:21]
        result = get_result(lower, higher)
        
        result_file = open("result_file.csv","w")
        if lower == higher:
            if len(result) == 1:
                for row in result:
                    result_file.write('"'+str(row["date"])+'",'+str(row["rain"])+"\n")
            else:
                for row in result:
                    result_file.write('"'+str(row["hour"])+'",'+str(row["rain"])+"\n")
        else:
            dates = []
            for row in result:
                if not row["date"] in dates:
                    dates.append(row["date"])
                    rain = 0
                    for hourRow in result:
                        if hourRow["date"] == row["date"]:
                            rain = rain + hourRow["rain"]
                    result_file.write('"'+row["date"]+'",'+str(rain)+"\n")
        result_file.close()

        status_finished()

    if msg.topic == 'gui_request/temp':
        lower = decoded[0:10]
        higher = decoded[11:21]
        result = get_result(lower, higher)

        result_file = open("result_file.csv","w")
        if lower == higher:
            if len(result) == 1:
                for row in result:
                    result_file.write('"'+str(row["date"])+'",'+str(row["temp"])+"\n")
            else:
                for row in result:
                    result_file.write('"'+str(row["hour"])+'",'+str(row["temp"])+"\n")
        else:
            dates = []
            for row in result:
                if not row["date"] in dates:
                    dates.append(row["date"])
                    counter = temp = 0
                    for hourRow in result:
                        if hourRow["date"] == row["date"]:
                            counter = counter + 1
                            temp = temp + float(hourRow["temp"])
                    result_file.write('"'+row["date"]+'",'+str(temp/counter)+"\n")
        result_file.close()

        status_finished()

    if msg.topic == 'gui_request/press':
        lower = decoded[0:10]
        higher = decoded[11:21]
        result = get_result(lower, higher)

        result_file = open("result_file.csv","w")
        if lower == higher:
            if len(result) == 1:
                for row in result:
                    result_file.write('"'+str(row["date"])+'",'+str(row["press"])+"\n")
            else:
                for row in result:
                    result_file.write('"'+str(row["hour"])+'",'+str(row["press"])+"\n")
        else:
            dates = []
            for row in result:
                if not row["date"] in dates:
                    dates.append(row["date"])
                    counter = press = 0
                    for hourRow in result:
                        if hourRow["date"] == row["date"]:
                            counter = counter + 1
                            press = press + hourRow["press"]
                    result_file.write('"'+row["date"]+'",'+str(press/counter)+"\n")
        result_file.close()

        status_finished()

    if msg.topic == 'gui_request/wind':
        lower = decoded[0:10]
        higher = decoded[11:21]
        result = get_result(lower, higher)

        result_file = open("result_file.csv","w")
        if lower == higher:
            if len(result) == 1:
                for row in result:
                    result_file.write('"'+str(row["date"])+'",'+str(row["wind"])+"\n")
            else:
                for row in result:
                    result_file.write('"'+str(row["hour"])+'",'+str(row["wind"])+"\n")
        else:
            dates = []
            for row in result:
                if not row["date"] in dates:
                    dates.append(row["date"])
                    counter = wind = 0
                    for hourRow in result:
                        if hourRow["date"] == row["date"]:
                            counter = counter + 1
                            wind = wind + hourRow["wind"]
                    result_file.write('"'+row["date"]+'",'+str(wind/counter)+"\n")
        result_file.close()

        status_finished()

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
