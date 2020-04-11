#mqtt client import
import paho.mqtt.client as mqtt
import weather_api
import time

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
        msg = weather_api.get_avg_tmps_form_year(2018)
        msg += weather_api.get_avg_tmps_form_year(2019)
        msg += weather_api.get_avg_tmps_form_year(2020)
        client.publish("test_topic", msg)
        time.sleep(120)
finally:
    client.loop_stop()
