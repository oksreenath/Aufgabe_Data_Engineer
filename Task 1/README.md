This sub-repository contains the Python code to do an API call from the website www.marinetraffic.com \
It also contains the Python code to load the CSV data into the database.\
The Database uses a PostgresSQL container pulled from Dockerhub.\
\
**Prerequisites**
* Docker & Python 3 installed
* Python libraries requests & psycopg2 (PostgresSQL client for Python) installed.
* Please pull the PostgresSQL image using the command `docker pull postgres`
* Once the image is pulled, please run the container using the command `docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres`
\
\
Run the Marine_Traffic_API.py file using the command `python3 Marine_Traffic_API.py`\
The user can choose between\
1. Call the Marine Traffic API.
2. Insert the values directly into the Database.
3. Exit the Python program.\
\
If the user chooses option 1, the API call to Marine Traffic website is made and the response is stored inside the Database. The program creates a database named marinetraffic and creates the table named ship_positions.\
\
If the user chooses option 2, the user is prompted to input the values for each column manually. These values are then passed to the ship_positions table.
\
\
This sub-repository also contains the Python file Load_Data.py. This script is used to upload the data in the csv files 'ship_engines.csv', 'ships_per_owner.csv' & 'position_data.csv' to the database.\
The script produces a file named 'ships_per_owner_pivoted.csv' which is derived from the file 'ships_per_owner.csv'. 
The database will be populated with the following tables:
**position_data**\
![Image](/Aufgabe_Data_Engineer/Images/Position_Data.png?raw=true)
* ship_engines
* ship_owners

