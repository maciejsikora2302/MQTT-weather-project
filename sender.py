import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("I manage to connect to server")
    else:
        print("Something went wrong with connecting, rc = ", rc)
def on_log(client, userdata, level, buf):
    print("Log: ", buf)

brooker = "127.0.0.1"
client = mqtt.Client("test_client")

client.on_connect = on_connect
client. on_log = on_log

client.connect(brooker)
client.loop_start()
client.loop_stop()
