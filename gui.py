from guietta import Gui, _, R1, ___, M, Ax, III
import paho.mqtt.client as mqtt
import datetime as dt
from time import sleep
import matplotlib.pyplot as plt
import numpy as np

request_ready = False
suback = False

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

    global request_ready

    if msg.topic == "request_status" and decoded == "done":
        request_ready = True

def is_request_ready():
    status_file = open("status.txt", "r")
    file_content = status_file.read()
    if file_content == "ready":
        status_file.close()
        open("status.txt", "w").close()
        return True
    else:
        return False

def get_datatype_and_dates(gui):
    data_type = "gui_request/"
    if gui.Deszcz.isChecked():
        data_type += "rain"
    elif gui.Temperatura.isChecked():
        data_type += "temp"
    elif gui.Wiatr.isChecked():
        data_type += "wind"
    elif gui.Cisnienie.isChecked():
        data_type += "press"
    else:
        raise ValueError

    #format rrrr-mm-dd



    separator = "-"


    def create_date(day, month, year, separator):
        result_date = ""
        result_date += year + separator

        tmp = ""
        if month in "123456789":
            tmp += "0" + month
        else:
            tmp = month
        result_date += tmp + separator

        tmp = ""
        if day in "123456789":
            tmp += "0" + day
        else:
            tmp = month
        result_date += tmp

        return result_date

    start_date = create_date(gui.Day1, gui.Month1, gui.Year1, separator)
    end_date = create_date(gui.Day2, gui.Month2, gui.Year2, separator)

    try:
        d1 = dt.datetime(int(gui.Year1), int(gui.Month1), int(gui.Day1))
        d2 = dt.datetime(int(gui.Year2), int(gui.Month2), int(gui.Day2))

        if d2 < d1:
            error = Gui(["Data końcowa jest przed datą początkową"])
            error.run()
    except ValueError:
        error = Gui(["Jedna z dat jest błędna"])
        error.run()

    # print(data_type, start_date, end_date)
    # print("Connecting to MQTT brooker")

    brooker = "127.0.0.1"
    client = mqtt.Client("gui")

    client.on_connect = on_connect
    client.on_log = on_log
    client.on_message = on_messege

    client.connect(brooker)
    client.subscribe("request_status")

    try:
        client.loop_start()

        global request_ready
        request_ready = False

        client.publish(data_type, start_date + " " + end_date)
        while not request_ready:
            print("Waiting for request to be ready...")
            sleep(0.1)
    finally:
        client.loop_stop()

    res_file = open("result_file.csv", "r")

    data = []
    value = []

    for line in res_file.readlines():
        l = line.strip("\n").split(",")
        data.append(l[0])
        value.append(float(l[1]))

    res_file.close()

    plot = Gui(
        [M('plot', width=10, height=10), ___],
        [III, III],
        [_, _]
               )

    def replot(gui):
        with Ax(gui.plot) as ax:
            ax.set_title('Data visualiser')
            ax.plot(data, value, ".-")
            plt.setp(ax.get_xticklabels(), rotation=45)
            ax.set_autoscale_on(True)
            # ax.set_xtickslabels(data, rotation="vertical")



    replot(plot)
    plot.run()









gui = Gui(
    ["MQTT Weather Project", ___, ___, ___, ___],
    ["Wprowadź zakres dat", _, _, _, _],
    ["Początek", "__Day1__", "__Month1__", "__Year1__", _],
    ["Koniec", "__Day2__", "__Month2__", "__Year2__", _],
    ["Zaznacz typ danych:", R1("Deszcz"), R1("Temperatura"), R1("Wiatr"), R1("Cisnienie")],
    [["Zwizualizuj"], ___, ___, ___, ___]
)


# gui.Day1 = "Dzień"
# gui.Month1 = "Miesiąc"
# gui.Year1 = "Rok"
#
# gui.Day2 = "Dzień"
# gui.Month2 = "Miesiąc"
# gui.Year2 = "Rok"

gui.Day1 = "2"
gui.Month1 = "2"
gui.Year1 = "2020"

gui.Day2 = "8"
gui.Month2 = "2"
gui.Year2 = "2020"



gui.Zwizualizuj = get_datatype_and_dates


gui.run()

















# import paho.mqtt.client as mqtt
#
# def on_connect(client, userdata, flags, rc):
#     if rc == 0:
#         print("I manage to connect to server")
#     else:
#         print("Something went wrong with connecting, rc = ", rc)
# def on_log(client, userdata, level, buf):
#     print("Log: ", buf)
#
# def on_messege(client, userdata, msg):
#     decoded = msg.payload.decode("utf-8")
#     print(f"Message I received -> Topic: {msg.topic}, Message: {decoded}")
#
# brooker = "127.0.0.1"
# client = mqtt.Client("operator")
#
# client.on_connect = on_connect
# client.on_log = on_log
# client.on_message = on_messege
#
# client.connect(brooker)
#
# try:
#     while True:
#         client.loop_start()
# finally:
#     client.loop_stop()