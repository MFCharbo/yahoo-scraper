
import mysql.connector
from mysql.connector import Error
import json
from dateutil import parser
import time

import configparser

class Config:

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('api_info.ini')
        self.consumer_key = config['API_INFO']['CONSUMER_KEY']
        self.consumer_secret = config['API_INFO']['CONSUMER_SECRET']
        self.access_token = config['API_INFO']['ACCESS_TOKEN']
        self.access_token_secret = config['API_INFO']['ACCESS_TOKEN_SECRET']
        self.password = config['API_INFO']['PASSWORD']

#Change this to use the class. 
consumer_key = Config().consumer_key
consumer_secret = Config().consumer_secret
access_token = Config().access_token
access_token_secret = Config().access_token_secret
password = Config().password

def connect(data):
    """
    connect to MySQL database and insert twitter data
    """

    try:
        con = mysql.connector.connect(host = 'localhost',
        database='Finance', user='root', password = password, charset = 'utf8')


        if con.is_connected():            
        
            cursor = con.cursor()
            for element in data:
                formated_date = parser.parse(element.get("date1")).date()
                company = element.get("company")
                if(element.get("volume1")):
                    formated_open = float(element.get("open1").replace(',',''))
                    formated_high = float(element.get("high1").replace(',',''))
                    formated_low = float(element.get("low1").replace(',',''))
                    formated_close = float(element.get("close1").replace(',',''))
                    formated_adj_close = float(element.get("adj_close").replace(',',''))
                    formated_volume = int(element.get("volume1").replace(',',''))
                    query = "INSERT INTO stocks (date, open, high, low, close, adj_close, volume, company) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.execute(query, (formated_date, formated_open, formated_high, formated_low, formated_close, formated_adj_close, formated_volume, company ))
                elif(not element.get("volume1")):
                    action = element.get("action") 
                    ratio_list =  element.get("ratio").split(":")
                    formated_ratio = float(ratio_list[0])/float(ratio_list[1])
                    query = "INSERT INTO stockActions (date, company, action, ratio) VALUES (%s, %s, %s, %s)"
                    cursor.execute(query, (formated_date, company, action, formated_ratio))
            con.commit()


    except Error as e:
        print(e)

        cursor.close()
        con.close()

    return

def store_to_database():
    with open('./financial.json') as f:
        data = json.load(f)
    connect(data)

store_to_database()