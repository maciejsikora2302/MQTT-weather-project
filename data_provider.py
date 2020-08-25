#mqtt client import
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
client = mqtt.Client("data_provider")

client.on_connect = on_connect
client.on_log = on_log
client.on_message = on_messege

client.connect(brooker)
# client.subscribe("test_topic")
try:
    while True:
        client.loop_start()
        record = get_json_from_imgw()
        date = record["data_pomiaru"] + " " + record["godzina_pomiaru"]
        msg = date + record["temperatura"]
        print(msg)
        client.publish("krakow/temp", msg)
        msg = date + record["predkosc_wiatru"]
        print(msg)
        client.publish("krakow/wind", msg)
        msg = date + record["cisnienie"]
        print(msg)
        client.publish("krakow/press", msg)
        msg = date + record["suma_opadu"]
        print(msg)
        client.publish("krakow/rain", msg)

        # wiadomość dla bazy - nie chciałem usuwać tego co napisałeś wcześniej
        # format np: "{"date": "2020-05-15", "hour": 14, "temp": 8.6, "wind": 3, "press": 1016.4, "rain": 1.4}"

        msg = "{'date': '" + record["data_pomiaru"]
        msg += "', 'hour': " + record["godzina_pomiaru"]
        msg += ", 'temp': " + record["temperatura"]
        msg += ", 'wind': " + record["predkosc_wiatru"]
        msg += ", 'press': " + record["cisnienie"]
        msg += ", 'rain': " + record["suma_opadu"] + "}"
        print(msg)
        client.publish("krakow/fillDatabase", msg)

        time.sleep(3600)
finally:
    client.loop_stop()

