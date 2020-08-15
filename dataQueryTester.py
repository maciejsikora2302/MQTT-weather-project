import time
from tinydb import TinyDB, Query
import json
import ast

db = TinyDB('db.json')
query = Query()

def insert_test_data():
    db.insert({"date": "2020-01-01", "hour": 8, "temp": 9.8, "wind": 5, "press": 1015.8, "rain": 1.4})
    db.insert({"date": "2020-01-01", "hour": 9, "temp": 9.8, "wind": 5, "press": 1015.8, "rain": 1.4}) 
    db.insert({"date": "2020-01-01", "hour": 10, "temp": 9.8, "wind": 5, "press": 1015.8, "rain": 1.4})
    db.insert({"date": "2019-12-31", "hour": 8, "temp": 9.8, "wind": 5, "press": 1015.8, "rain": 1.4})
    db.insert({"date": "2019-12-31", "hour": 9, "temp": 9.8, "wind": 5, "press": 1015.8, "rain": 1.4})
    db.insert({"date": "2019-12-31", "hour": 10, "temp": 9.8, "wind": 5, "press": 1015.8, "rain": 1.4})

# result's type is str

def get_info(type, condition):
    print(f"EQUAL Type {type}, condition {condition}")
    result = db.search(query[type] == condition)
    print(result)

def get_greater_info(type, condition):
    print(f"GREATER Type {type}, condition {condition}")
    result = db.search(query[type] > condition)
    print(result)

def get_lower_info(type, condition):
    print(f"LOWER Type {type}, condition {condition}")
    result = db.search(query[type] < condition)
    print(result)

def get_middle_info(type, lower, higher):
    print(f"MIDDLE Type {type}, lower {lower} ,higher {higher}")
    result = db.search((lower < query[type]) & (query[type] < higher))
    print(result)

def run_all():
    # insert_test_data()

    get_info("date","2020-05-15")
    print("date test1")
    get_lower_info("date","2020-01-02")
    get_greater_info("date","2020-01-02")
    get_lower_info("date","2019-12-31")
    get_greater_info("date","2019-12-31")
    print("date test2")
    get_lower_info("date","2021")
    get_greater_info("date","2021")
    get_lower_info("date","2020-06")
    get_greater_info("date","2020-04")
    print("hour test")
    get_lower_info("hour",10)
    get_greater_info("hour",10)
    get_lower_info("hour",8)
    get_greater_info("hour",8)
    print("temp test")
    get_lower_info("temp",20)
    get_greater_info("temp",20)
    get_lower_info("temp",0)
    get_greater_info("temp",0)
    print("middle test")
    get_middle_info("wind",1,5)
    get_middle_info("press",2,6)
    get_middle_info("rain",1,5)

run_all()

# all methods worked as expected