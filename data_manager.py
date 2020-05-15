import paho.mqtt.client as mqtt
import time
from tinydb import TinyDB, Query
import json
import ast

db = TinyDB('db.json')
query = Query()

def search_equal(type, value):
    print(db.search(query[type] == value))

def search_greater(type, value):
    print(db.search(query[type] > value))

def search_lower(type, value):
    print(db.search(query[type] < value))

def search_in_range(type, lower, higher):
    print(db.search((lower < query[type]) & (query[type] < higher)))

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
        print(type(newDict))
        if not db.contains((query.date == newDict.get("date")) & (query.hour == newDict.get("hour"))):
            db.insert(newDict)
            print("Inserted")
        else:
            print("Already exists")

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
