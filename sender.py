#mqtt client import
import paho.mqtt.client as mqtt
import weather_api
# importlib.import_module("weather_api")

# def get_daily

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


weather_api.get_info_form_year(2019)

brooker = "127.0.0.1"
client = mqtt.Client("sender")

client.on_connect = on_connect
client.on_log = on_log
client.on_message = on_messege

client.connect(brooker)
# client.subscribe("test_topic")
client.loop_start()
client.publish("test_topic", "first msg with special signs ;'-=>,;")
client.loop_stop()
