import json
import logging
from pymongo import MongoClient

client=None
file=open('config.json')
config=json.load(file)

def get_database():
    try:
        CONNECTION_STRING = "mongodb+srv://"+config['username']+":"+config['password']+"@"+config['host']+"/myFirstDatabase?retryWrites=true&w=majority"
        clients = MongoClient(CONNECTION_STRING)
        tbl=config['dbname']
        return clients[tbl]
    except Exception as err:
        logging.error(f'Error while opening database connection: {err}')
        return False
def close_connection():
    try:
        client.close()
        return True
    except Exception as err:
        logging.error(f'Error while closing database connection: {err}') #Need to add logger here
        return False


if __name__=="__main__":
    get_database()