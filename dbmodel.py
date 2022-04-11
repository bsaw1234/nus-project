import datetime
import requests
import json
from dblayer import *

file=open('config.json')
config=json.load(file)

def insert_stockData():
    dbname = get_database()
    collection_name = dbname[config['tbl_name']]
    response_API = requests.get(config['stock_api'])
    stock_data=response_API.json()
    stock_data['created_date']=datetime.datetime.now()
    print(stock_data)
    collection_name.insert_many([stock_data])

def get_stockData():
    dbname = get_database()
    collection_name = dbname[config['tbl_name']]
    res=collection_name.find()
    for r in res:
        print(r)




if __name__=="__main__":
    #insert_stockData()
    get_stockData()
