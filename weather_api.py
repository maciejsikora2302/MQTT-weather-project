#needed to make web requests
import requests
#store the data we get as a dataframe
import pandas as pd
#convert the response as a strcuctured json
import json
#mathematical operations on lists
import numpy as np
#parse the datetimes we get from NOAA
from datetime import datetime
import matplotlib.pyplot as plt
import pprint as pp



def get_avg_tmps_form_year(year):
    #add the access token you got from NOAA
    Token = 'mStylOOJxTfWQyldIPzewknBewZXQrIq'

    #Long Beach Airport station
    station_id = 'GHCND:USW00023129'

    # initialize lists to store data
    dates_temp = []
    temps = []

    # for each year from 2015-2019 ...
    # for year in range(2015, 2020):
    year = str(year)
    print('working on year ' + year)

    # make the api call
    r = requests.get(
        'https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TAVG&limit=1000&stationid=GHCND:USW00023129&startdate=' + year + '-01-01&enddate=' + year + '-12-31',
        headers={'token': Token})
    # r = requests.get("https://www.ncdc.noaa.gov/cdo-web/api/v2/datatypes", headers = {'token': Token})
    # load the api response as a json
    d = json.loads(r.text)
    # get all items in the response which are average temperature readings
    avg_temps = [item for item in d['results'] if item['datatype'] == 'TAVG']
    # get the date field from all average temperature readings
    dates_temp += [item['date'] for item in avg_temps]
    # get the actual average temperature from all average temperature readings
    temps += [item['value'] for item in avg_temps]

    return_str = ""
    for val in zip(dates_temp, temps):
        return_str += str(val[0])
        return_str += ';'
        return_str += str(val[1])
        return_str += ';'
    return return_str