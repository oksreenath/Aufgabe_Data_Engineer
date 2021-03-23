This sub-repository contains the python file Crawler.py to crawl the webpage [www.finning.com](https://www.finning.com/en_CA/products/new/power-systems/electric-power-generation.html) \
Similar to Task 1, the PostgresSQL database is running on docker.\
\
**Prerequisites**
* Chrome installed
* Docker & Python 3 installed.
* Python libraries selenium & psycopg2 installed.
* Please pull the PostgresSQL image using the command `docker pull postgres`
* Once the image is pulled, please run the container using the command `docker run --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres -d postgres`
* The bin folder contains the web drivers for selenium. Please place the bin folder in the same folder as the Crawler.py file.
\
Run the Crawler.py file using the command `python3 Crawler.py`\
The python script will open up a chrome browser pointing to the web page where the list of motors are present.\
The script automatically opens each motor webpage, read the required specifications and send them to the table named motors.\
The script uses a combination of selenium and xpath to do the web crawling.
Once the motor specifications are read, The script goes back to the previous page and iterates over all the motors in the webpage.\
This process is repeated until page number 13 (the last page).\
The columns created in the motors table are:
1. product_id
2. frequency
3. voltage
4. min_rating
5. max_rating
6. min_speed
7. max_speed
\
\
The speed attribute is split into min_speed and max_speed as some engines contains two different speed measurements. If there is only one speed specified, both the columns contains the same speed.