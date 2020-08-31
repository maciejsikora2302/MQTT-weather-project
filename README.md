# MQTT-weather-project
Project for Pyhon programming involving MQTT communication and displaying weather conditions

# Instalacja wymaganych bibliotek
```shell script
pip install paho-mqtt 
pip install pandas 
pip install guietta 
pip install tinydb
```

# Uruchomienie
Przeprowadzenie symulacji wymaga uprzedniego uruchomienia brokera MQTT zawartego w plikach projektu. \
Następnym krokiem jest uruchomienie w osobnych terminalach data_manager.py oraz gui.py, między którymi to odbywa się komunikacja z wykorzystaniem brokera. \
W uruchomionym okienku gui można wybrać przedział czasu, z którego mają zostać wyświetlone dane oraz ich rodzaj, do wyboru jest temperatura, deszcz, prędkość wiatru i ciśnienie. \
Dane pochodzą ze stacji meteorologicznej Kraków-Balice. 

# Dane
Baza danych może zostać zaktualizowana pobierając dane bezpośrednio z API stacji. \
W tym celu wymagane jest użycie brokera oraz uruchomienie w osobnych terminalach data_manager.py oraz data_provider.py (ważne jest uruchomienie w tej kolejności, ponieważ data_provider od razu rozpoczyna przesyłanie danych). \
Aktualnie w bazie dostępne są dane włącznie od stycznia do lipca 2020.

