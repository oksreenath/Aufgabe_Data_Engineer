import requests
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import datetime
def call_api():
    print("Calling PS01-API from MarineTraffic")
    try:
        #response = requests.get('htthttps://services.marinetraffic.com/api/exportvesseltrack/631820efd957bc0869644ad2753d969118be4b15/v:3/fromdate:2021-01-01 01:01:01/todate:2021-01-01 01:06:02/mmsi:269057489/protocol:jsono')
        response = [{'MMSI': '269057489', 'IMO': '0', 'STATUS': '5', 'SPEED': '0', 'LON': '6.987368', 'LAT': '50.973230',
                 'COURSE': '22', 'HEADING': '88', 'TIMESTAMP': '2021-01-01T01:05:49', 'SHIP_ID': '330455'},
                {'MMSI': '269057489', 'IMO': '0', 'STATUS': '5', 'SPEED': '0', 'LON': '6.987375', 'LAT': '50.973230',
                 'COURSE': '22', 'HEADING': '89', 'TIMESTAMP': '2021-01-01T01:26:49', 'SHIP_ID': '330455'}]
        #data = response.json()
        return response
    except Exception as e:
        print(e)


def connect_to_db(response):
    db_name = "marinetraffic"
    user = "postgres"
    host = "localhost"
    password = "postgres"
    table_name = "ship_positions"
    check_for_db(db_name=db_name)

    conn = psycopg2.connect(dbname=db_name, user=user, host=host, password=password)
    cur = conn.cursor()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    #cur.execute('DROP TABLE IF EXISTS ' + table_name)
    cur.execute('CREATE TABLE IF NOT EXISTS ' + table_name + '(MMSI INT, IMO INT, STATUS INT, SPEED INT, LON FLOAT(10), LAT FLOAT(10), COURSE INT, HEADING INT, TIMESTAMP TIMESTAMP PRIMARY KEY, SHIP_ID INT);')

    columns_names = ['MMSI', 'IMO', 'STATUS', 'SPEED', 'LON', 'LAT', 'COURSE', 'HEADING', 'TIMESTAMP', 'SHIP_ID']
    columns_names_str = ','.join(columns_names)
    binds_str = ','.join('%s' for _ in range(len(columns_names)))

    for data_dict in response:
        sql = ('INSERT INTO '+ table_name + '({columns_names}) VALUES ({binds})'.format(columns_names=columns_names_str,binds=binds_str))
        values = [data_dict[column_name] for column_name in columns_names]
        try:
            cur.execute(sql, values)
        except Exception as e:
            print(e)
    conn.commit()
    cur.close()
    conn.close()

def insert_into_db():
    mmsi = input("Please enter the MMSI: ")
    mmsi = int(mmsi)
    imo = input("Please enter imo: ")
    imo = int(imo)
    status = input("Please enter the status: ")
    status = int(status)
    speed = input("Please enter the speed: ")
    speed = int(speed)
    lon = input("Please enter the Longitude: ")
    lon = float(lon)
    lat = input("Please enter the latitude: ")
    lat = float(lat)
    course = input("Please enter the course: ")
    course = int(course)
    heading = input("Please enter the heading: ")
    heading = int(heading)
    time = input("Please enter the timestamp: YYYY-MM-DD HH:MM:SS ")
    time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    id = input("Please enter the ship id: ")
    id = int(id)

    db_name = "marinetraffic"
    user = "postgres"
    host = "localhost"
    password = "postgres"
    table_name = "ship_positions"
    check_for_db(db_name=db_name)

    conn = psycopg2.connect(dbname=db_name, user=user, host=host, password=password)
    cur = conn.cursor()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # cur.execute('DROP TABLE IF EXISTS ' + table_name)
    cur.execute(
        'CREATE TABLE IF NOT EXISTS ' + table_name + '(MMSI INT, IMO INT, STATUS INT, SPEED INT, LON FLOAT(10), LAT FLOAT(10), COURSE INT, HEADING INT, TIMESTAMP TIMESTAMP PRIMARY KEY, SHIP_ID INT);')

    columns_names = ['MMSI', 'IMO', 'STATUS', 'SPEED', 'LON', 'LAT', 'COURSE', 'HEADING', 'TIMESTAMP', 'SHIP_ID']
    values = [mmsi, imo, status, speed, lon, lat, course, heading, time, id]
    columns_names_str = ','.join(columns_names)
    # values_str = ','.join(values)
    binds_str = ','.join('%s' for _ in range(len(columns_names)))


    # cur.execute('INSERT INTO ' + table_name + '(PRODUCT_ID, FREQUENCY, VOLTAGE, MIN_RATING, MAX_RATING, SPEED) VALUES('+product_id+','+frequency+','+voltage+','+min_rating+','+max_rating+','+speed+')')
    sql = ('INSERT INTO ' + table_name + '({columns_names}) VALUES ({binds})'.format(columns_names=columns_names_str,
                                                                                     binds=str(binds_str)))
    try:
        cur.execute(sql, values)
        print("Database successfully updated with the input values")
    except Exception as e:
        print(e)
    return

def check_for_db(db_name):
    db_exists = False
    user = "postgres"
    host = "localhost"
    password = "postgres"
    conn_test = psycopg2.connect(dbname="postgres", user=user, host=host, password=password)
    cur_test = conn_test.cursor()
    conn_test.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur_test.execute("SELECT datname FROM pg_database;")
    list_database = cur_test.fetchall()
    for i in list_database:
        if db_name in str(i):
            db_exists = True
    if not db_exists:
        cur_test.execute('CREATE DATABASE ' + db_name)
        print("Database "+db_name+" created")
    conn_test.commit()
    cur_test.close()
    conn_test.close()
    return


if __name__ == "__main__":
    while True:
        value = input("Please choose between the following\n1. Call MarineTraffic API\n2. Manually enter values to the Database\n3. Exit\nEnter the value: ")
        value = int(value)
        if value == 1:
            response = call_api()
            if response:
                connect_to_db(response)
        elif value == 2:
            insert_into_db()
        elif value == 3:
            exit()
        else:
            print("Incorrect value")

# db_name = "marinetraffic"
# user = "postgres"
# host = "localhost"
# password = "postgres"
# table_name = "ship_positions"
# conn = psycopg2.connect(dbname =db_name, user=user, host=host, password=password)
# cur = conn.cursor()
#
# columns_names = ['MMSI', 'IMO', 'STATUS', 'SPEED', 'LON', 'LAT', 'COURSE', 'HEADING', 'TIMESTAMP', 'SHIP_ID']
# columns_names_str = ','.join(columns_names)
# #print(columns_names_str)
#
# binds_str = ','.join('%s' for _ in range(len(columns_names)))
#
# for data_dict in data:
#     sql = ('INSERT INTO '+ table_name + '({columns_names}) VALUES ({binds})'.format(columns_names=columns_names_str,binds=binds_str))
#     values = [data_dict[column_name] for column_name in columns_names]
#     try:
#         cur.execute(sql, values)
#     except Exception as e:
#         print(e)

# cur.execute("SELECT datname FROM pg_database;")
# list_database = cur.fetchall()

#cur.execute('DROP DATABASE IF EXISTS '+ db_name)
#cur.execute('CREATE DATABASE '+ db_name)

# cur.execute('DROP TABLE IF EXISTS ' + table_name)
# cur.execute('CREATE TABLE ' + table_name + '(MMSI INT, IMO INT, STATUS INT, SPEED INT, LON FLOAT(10), LAT FLOAT(10), COURSE INT, HEADING INT, TIMESTAMP TIMESTAMP PRIMARY KEY, SHIP_ID INT);')
# conn.commit()
# cur.close()
# conn.close()


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
#data = [{'MMSI': '269057489', 'IMO': '0', 'STATUS': '5', 'SPEED': '0', 'LON': '6.987368', 'LAT': '50.973230', 'COURSE': '22', 'HEADING': '88', 'TIMESTAMP': '2021-01-01T01:05:48', 'SHIP_ID': '330455'}, {'MMSI': '269057489', 'IMO': '0', 'STATUS': '5', 'SPEED': '0', 'LON': '6.987375', 'LAT': '50.973230', 'COURSE': '22', 'HEADING': '89', 'TIMESTAMP': '2021-01-01T01:26:48', 'SHIP_ID': '330455'}]
# print(len(data))

