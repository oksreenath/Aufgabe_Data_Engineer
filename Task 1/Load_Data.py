import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pandas

db_exists = False
db_name = "marinetraffic"
user = "postgres"
host = "localhost"
password = "postgres"
table_name_position = "position_data"
table_name_engines = "ship_engines"
table_name_owners = "ships_owners"

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
conn_test.commit()
cur_test.close()
conn_test.close()

conn = psycopg2.connect(dbname=db_name, user=user, host=host, password=password)
cur = conn.cursor()
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur.execute('DROP TABLE IF EXISTS ' + table_name_position)
cur.execute('DROP TABLE IF EXISTS ' + table_name_engines)
cur.execute('DROP TABLE IF EXISTS ' + table_name_owners)
cur.execute('CREATE TABLE IF NOT EXISTS ' + table_name_engines + '(MMSI INT, SHIP_NAME VARCHAR, ENGINE1_ID VARCHAR, ENGINE1_NAME VARCHAR, ENGINE2_ID VARCHAR, ENGINE2_NAME VARCHAR, ENGINE3_ID VARCHAR, ENGINE3_NAME VARCHAR, PRIMARY KEY(SHIP_NAME));')
cur.execute('CREATE TABLE IF NOT EXISTS ' + table_name_owners + '(SHIP_ID VARCHAR, OWNERS VARCHAR, PRIMARY KEY(SHIP_ID));')
cur.execute('CREATE TABLE IF NOT EXISTS ' + table_name_position + '(SHIP VARCHAR, TIMESTAMPS TIMESTAMP, SPEED INT, LON FLOAT(10), LAT FLOAT(10), CONSTRAINT fk_ship FOREIGN KEY(SHIP) REFERENCES ships_owners(SHIP_ID));')

#ships_per_owner.csv file is copied to a dataframe to pivot and saved back as a .csv file.

df = pandas.read_csv('ships_per_owner.csv')
ship_id = []
owner = []
for i in range(0,5):
    for index, row in df.iterrows():
        ship_id.append(row[i])
        owner.append(df.columns[i])
data_tuples = list(zip(ship_id, owner))
ships_per_owner = pandas.DataFrame(data_tuples, columns=['SHIP_ID', 'OWNERS'])
ships_per_owner = ships_per_owner.dropna(axis=0, how="any")
ships_per_owner.to_csv("ships_per_owner_pivoted.csv", index=False)

#The csv files are opened and the values are passed to the corresponding tables.

with open('ships_per_owner_pivoted.csv','r') as f:
    next(f)
    cur.copy_from(f,'ships_owners', sep=',')
with open('position_data.csv','r') as f:
    next(f)
    cur.copy_from(f, 'position_data', sep=',')
with open('ship_engines.csv','r') as f:
    next(f)
    cur.copy_from(f, 'ship_engines', sep=',')
conn.commit()
cur.close()
conn.close()

