from guietta import Gui, _, R1, ___
import datetime as dt

def get_datatype_and_dates(gui):
    data_type = "/visualizer/"
    if gui.Deszcz.isChecked():
        data_type += "rain"
    elif gui.Temperatura.isChecked():
        data_type += "tmp"
    elif gui.Wiatr.isChecked():
        data_type += "wind"
    else:
        raise ValueError

    #format rrrr-mm-dd

    separator = "-"

    start_date = ""
    start_date += gui.Year1 + separator
    start_date += gui.Month1 + separator
    start_date += gui.Day1

    end_date = ""
    end_date += gui.Year2 + separator
    end_date += gui.Month2 + separator
    end_date += gui.Day2

    try:
        d1 = dt.datetime(int(gui.Year1), int(gui.Month1), int(gui.Day1))
        d2 = dt.datetime(int(gui.Year2), int(gui.Month2), int(gui.Day2))

        if d2 < d1:
            error = Gui(["Data końcowa jest przed datą początkową"])
            error.run()
    except ValueError:
        error = Gui(["Jedna z dat jest błędna"])
        error.run()

    print(data_type, start_date, end_date)



gui = Gui(
    ["MQTT Weather Project", ___, ___, ___],
    ["Wprowadź zakres dat", _, _, _],
    ["Początek", "__Day1__", "__Month1__", "__Year1__"],
    ["Koniec", "__Day2__", "__Month2__", "__Year2__"],
    ["Zaznacz typ danych:", R1("Deszcz"), R1("Temperatura"), R1("Wiatr")],
    [["Zwizualizuj"], ___, ___, ___]
)


gui.Day1 = "Dzień"
gui.Month1 = "Miesiąc"
gui.Year1 = "Rok"

gui.Day2 = "Dzień"
gui.Month2 = "Miesiąc"
gui.Year2 = "Rok"


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