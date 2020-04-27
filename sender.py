#mqtt client import
import weather_api
import paho.mqtt.client as mqtt
import time
import json
import requests

def get_json_from_imgw():
    site = "https://danepubliczne.imgw.pl/api/data/synop/id/12566"
    r = requests.get(site)
    d = json.loads(r.text)
    return d

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

brooker = "127.0.0.1"
client = mqtt.Client("sender")

client.on_connect = on_connect
client.on_log = on_log
client.on_message = on_messege

client.connect(brooker)
# client.subscribe("test_topic")
try:
    while True:
        client.loop_start()
        record = get_json_from_imgw()
        date = record["data_pomiaru"] + ";" + record["godzina_pomiaru"] + ";"
        msg = date + record["temperatura"]
        client.publish("krakow/temp", msg)
        msg = date + record["predkosc_wiatru"]
        client.publish("krakow/wind", msg)
        msg = date + record["cisnienie"]
        client.publish("krakow/press", msg)
        msg = date + record["suma_opadu"]
        client.publish("krakow/rain", msg)
        time.sleep(5)
finally:
    client.loop_stop()
