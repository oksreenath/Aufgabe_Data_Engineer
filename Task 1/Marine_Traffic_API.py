
#Write python API for website.

import requests
from bs4 import BeautifulSoup as Soup
import json
import mysql.connector
import psycopg2
import time
#response = requests.get('https://services.marinetraffic.com/api/exportvesseltrack/7fc28b8a9945e061a7c4b141e9330459cd1e85f7/v:3/period:hourly/days:2/mmsi:269057489')
#response = requests.get('https://services.marinetraffic.com/api/exportvesseltrack/631820efd957bc0869644ad2753d969118be4b15/v:3/fromdate:2021-01-01 01:01:01/todate:2021-01-01 01:27:02/mmsi:269057489/protocol:jsono')
# response = """<?xml version="1.0" encoding="utf-8" standalone="no"?>
# <VESSELTRACK>
#   <POSITION MMSI="269057489" IMO="0" STATUS="5" SPEED="0" LON="6.987368" LAT="50.973230" COURSE="22" HEADING="88" TIMESTAMP="2021-01-01T01:05:48" SHIP_ID="330455"/>
#   <POSITION MMSI="269057489" IMO="0" STATUS="5" SPEED="0" LON="6.987375" LAT="50.973230" COURSE="22" HEADING="89" TIMESTAMP="2021-01-01T01:26:48" SHIP_ID="330455"/>
#   <POSITION MMSI="269057489" IMO="0" STATUS="5" SPEED="0" LON="6.987371" LAT="50.973240" COURSE="22" HEADING="88" TIMESTAMP="2021-01-01T01:47:47" SHIP_ID="330455"/>
# </VESSELTRACK>"""
# data = response.json()
# print(data)
data = [{'MMSI': '269057489', 'IMO': '0', 'STATUS': '5', 'SPEED': '0', 'LON': '6.987368', 'LAT': '50.973230', 'COURSE': '22', 'HEADING': '88', 'TIMESTAMP': '2021-01-01T01:05:48', 'SHIP_ID': '330455'}, {'MMSI': '269057489', 'IMO': '0', 'STATUS': '5', 'SPEED': '0', 'LON': '6.987375', 'LAT': '50.973230', 'COURSE': '22', 'HEADING': '89', 'TIMESTAMP': '2021-01-01T01:26:48', 'SHIP_ID': '330455'}]
# print(len(data))


# for i in range(0, len(data)):
#     for j in range(0,10):
#         print(data[i][j])
#Database



db_name = "marinetraffic"
user = "postgres"
host = "localhost"
password = "postgres"
table_name = "ship_positions"
conn = psycopg2.connect(dbname =db_name, user=user, host=host, password=password)
cur = conn.cursor()

columns_names = ['MMSI', 'IMO', 'STATUS', 'SPEED', 'LON', 'LAT', 'COURSE', 'HEADING', 'TIMESTAMP', 'SHIP_ID']
columns_names_str = ','.join(columns_names)
#print(columns_names_str)

binds_str = ','.join('%s' for _ in range(len(columns_names)))

for data_dict in data:
    sql = ('INSERT INTO '+ table_name + '({columns_names}) VALUES ({binds})'.format(columns_names=columns_names_str,binds=binds_str))
    values = [data_dict[column_name] for column_name in columns_names]
    cur.execute(sql, values)

# cur.execute("SELECT datname FROM pg_database;")
# list_database = cur.fetchall()

#cur.execute('DROP DATABASE IF EXISTS '+ db_name)
#cur.execute('CREATE DATABASE '+ db_name)

# cur.execute('DROP TABLE IF EXISTS ' + table_name)
# cur.execute('CREATE TABLE ' + table_name + '(MMSI INT, IMO INT, STATUS INT, SPEED INT, LON FLOAT(10), LAT FLOAT(10), COURSE INT, HEADING INT, TIMESTAMP TIMESTAMP, SHIP_ID INT);')
conn.commit()
cur.close()
conn.close()
