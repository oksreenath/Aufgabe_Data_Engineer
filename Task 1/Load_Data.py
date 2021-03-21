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
conn = psycopg2.connect(dbname=db_name, user=user, host=host, password=password)
cur = conn.cursor()
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur.execute("SELECT datname FROM pg_database;")
list_database = cur.fetchall()
for i in list_database:
    if "marinetraffic" in str(i):
        db_exists = True
# cur.execute('DROP DATABASE IF EXISTS '+ db_name)
if not db_exists:
    cur.execute('CREATE DATABASE ' + db_name)
cur.execute('DROP TABLE IF EXISTS ' + table_name_position)
cur.execute('DROP TABLE IF EXISTS ' + table_name_engines)
cur.execute('DROP TABLE IF EXISTS ' + table_name_owners)
cur.execute('CREATE TABLE IF NOT EXISTS ' + table_name_position + '(SHIP VARCHAR, TIMESTAMPS TIMESTAMP, SPEED INT, LON FLOAT(10), LAT FLOAT(10));')
cur.execute('CREATE TABLE IF NOT EXISTS ' + table_name_engines + '(MMSI INT, SHIP_NAME VARCHAR, ENGINE1_ID VARCHAR, ENGINE1_NAME VARCHAR, ENGINE2_ID VARCHAR, ENGINE2_NAME VARCHAR, ENGINE3_ID VARCHAR, ENGINE3_NAME VARCHAR);')
cur.execute('CREATE TABLE IF NOT EXISTS ' + table_name_owners + '(OWNER VARCHAR, SHIP_ID VARCHAR);')

df = pandas.read_csv('ships_per_owner.csv')
ship_id = []
owner = []
for i in range(0,5):
    for index, row in df.iterrows():
        ship_id.append(row[i])
        owner.append(df.columns[i])
data_tuples = list(zip(ship_id, owner))
ships_per_owner = pandas.DataFrame(data_tuples, columns=['SHIP_ID', 'OWNER'])
ships_per_owner = ships_per_owner.dropna(axis=0, how="any")
print(ships_per_owner)
ships_per_owner.to_csv("ships_per_owner_pivoted.csv", index=False)


with open('position_data.csv','r') as f:
    next(f)
    cur.copy_from(f, 'position_data', sep=',')
with open('ship_engines.csv','r') as f:
    next(f)
    cur.copy_from(f, 'ship_engines', sep=',')
with open('ships_per_owner_pivoted.csv','r') as f:
    next(f)
    cur.copy_from(f,'ships_owners', sep=',')
conn.commit()
cur.close()
conn.close()

