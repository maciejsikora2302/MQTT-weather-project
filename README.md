# MQTT-weather-project
Project for Pyhon programming involving MQTT communication and displaying weather conditions

# Instalation needed libraries
pip install paho-mqtt
pip install pandas
pip install guietta
pip install tinydb

# Uruchomienie
Przeprowadzenie symulacji wymaga uprzedniego uruchomienia brokera MQTT zawartego w plikach projektu. Następnym krokiem jest uruchomienie w osobnych terminalach data_manager.py oraz gui.py, między którymi to odbywa się komunikacja z wykorzystaniem brokera. W uruchomionym okienku gui można wybrać przedział czasu, z którego mają zostać wyświetlone dane oraz ich rodzaj. Dane pochodzą ze stacji meteorologicznej Kraków-Balice. 

# Dane
Bazę danych można aktualizować na 2 sposoby. Pierwszym sposobem jest pobieranie danych bezpośrednio (Maciek pomoż, nie wiem jak to nazwać xD). W tym celu wymagane jest użycie brokera oraaz uruchomienie w osobnych terminalach data_manager.py oraz data_provider.py (ważne jest uruchomienie w tej kolejności, ponieważ data_provider od razu rozpoczyna przesyłanie danych). Drugim sposobem jest wrzucenie pliku .csv w odpowiednim formacie ze strony danychpublicznych do folderu "2020_synop_csv", z którego program będzie pobierał pliki. Uruchomienie programu data_filler.py spowoduje wypełnienie bazy podanymi danymi.
