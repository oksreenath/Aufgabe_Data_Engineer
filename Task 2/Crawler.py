import os
import sys
#import requests
#from selenium.webdriver.common.keys import Keys
import time
import argparse
import logging.config
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
# from selenium.webdriver.common.action_chains import ActionChains
# from dateutil import parser as date_parser
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import TimeoutException
# from selenium.webdriver.support import expected_conditions as EC
click_next_counter = 0

logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s [PID %(process)d] [Thread %(thread)d] [%(levelname)s] [%(name)s] %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout"
        }
    },
    "root": {
        "level": "INFO",
        "handlers": [
            "console"
        ]
    }
})

website = "https://www.finning.com/en_CA/products/new/power-systems/electric-power-generation.html"


LOGGER = logging.getLogger()

def open_page(driver):
    driver.get(website)
    #driver.execute_script("document.body.style.zoom='50%'")
    return

def run(driver):
    try:
        open_page(driver=driver)
        open_product(driver=driver)
        #select_properties(driver=driver)
    except Exception as e:
        print(e)

    #driver.quit()

def select_properties(driver):
    time.sleep(4)
    try:
        id = "//*[@id='detail-section']/section[2]/div/div[2]/h1"
        product_id = driver.find_element_by_xpath(id).text
        print(product_id)
        freq = "//*[@id='tab2-1']/div/div[2]/div[2]/div[5]/span[2]"
        frequency = driver.find_element_by_xpath(freq).text
        print(frequency)
        vol = "//*[@id='tab2-1']/div/div[2]/div[2]/div[4]/span[2]"
        voltage = driver.find_element_by_xpath(vol).text
        print(voltage)
        min_rat = "//*[@id='tab2-1']/div/div[2]/div[2]/div[1]/span[2]"
        min_rating = driver.find_element_by_xpath(min_rat).text
        print(min_rating)
        max_rat = "//*[@id='tab2-1']/div/div[2]/div[2]/div[2]/span[2]"
        max_rating = driver.find_element_by_xpath(max_rat).text
        print(max_rating)
        sp = "//*[@id='tab2-1']/div/div[2]/div[2]/div[6]/span[2]"
        speed = driver.find_element_by_xpath(sp).text
        print(speed)
        if "or" in speed:
            min_speed = speed.split()[0]
            max_speed = speed.split()[2]
        else:
            min_speed = speed.split()[0]
            max_speed = speed.split()[0]

        driver.execute_script("window.history.go(-1)")
        # insert_to_db(product_id=product_id, frequency=frequency, voltage=voltage,
        #              min_rating=min_rating, max_rating=max_rating, min_speed=min_speed,
        #              max_speed=max_speed)
        time.sleep(2)
        return
    except Exception as e:
        print(e)
        return

def check_for_db(db_name):
    #Function for checking if the database marinetraffic exists.
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

def insert_to_db(product_id, frequency, voltage, min_rating,
                 max_rating, min_speed, max_speed):

    #Function for inserting the motor properties into the DB.
    db_name = "marinetraffic"
    user = "postgres"
    password = "postgres"
    host = "localhost"
    table_name = "motors"
    check_for_db(db_name)

    conn = psycopg2.connect(dbname=db_name, user=user, host=host, password=password)
    cur = conn.cursor()
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur.execute('CREATE TABLE IF NOT EXISTS '+ table_name +' (PRODUCT_ID VARCHAR, FREQUENCY VARCHAR, VOLTAGE VARCHAR, MIN_RATING VARCHAR, MAX_RATING VARCHAR, MIN_SPEED INT, MAX_SPEED INT);')
    columns_names = ['PRODUCT_ID', 'FREQUENCY', 'VOLTAGE', 'MIN_RATING', 'MAX_RATING', 'MIN_SPEED', 'MAX_SPEED']
    values = [product_id, frequency, voltage, min_rating, max_rating, min_speed, max_speed]
    columns_names_str = ','.join(columns_names)
    values_str = ','.join(values)
    binds_str = ','.join('%s' for _ in range(len(columns_names)))


    # cur.execute('INSERT INTO ' + table_name + '(PRODUCT_ID, FREQUENCY, VOLTAGE, MIN_RATING, MAX_RATING, SPEED) VALUES('+product_id+','+frequency+','+voltage+','+min_rating+','+max_rating+','+speed+')')
    sql = ('INSERT INTO ' + table_name + '({columns_names}) VALUES ({binds})'.format(columns_names=columns_names_str,
                                                                                     binds=str(binds_str)))
    cur.execute(sql, values)
    conn.commit()
    cur.close()
    conn.close()


def open_product(driver):
    global click_next_counter
    time.sleep(2)
    counter = 0

    #If the parser is on the last page, retrieve only the required motor specs and should not click on next.

    if click_next_counter == 13:
        #The for loop scrolls to the preferred view based on the item number, clicks on the motor based on the Xpath.
        for i in range(1,10):
            if i < 4:
                driver.execute_script("window.scrollTo(0, 600)")
            elif i > 3 and i < 7:
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, 1000)")
            elif i > 6 and i < 10:
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, 1700)")
                xpath = "//*[@id='product-family-page']/section[3]/div/div[2]/div/div[5]/article[" + str(
                    i) + "]/div/a[1]/h2"
                LOGGER.info("Clicking on product")
                time.sleep(2)
                driver.find_element_by_xpath(xpath).click()
                select_properties(driver)
                counter += 1

    elif click_next_counter < 13:
        for i in range(1,16):
            if i <4:
                driver.execute_script("window.scrollTo(0, 600)")
            elif i>3 and i<7:
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, 1000)")
            elif i>6 and i<10:
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, 1700)")
            elif i>9 and i<13:
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, 2400)")
            elif i>12:
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, 3100)")
            xpath = "//*[@id='product-family-page']/section[3]/div/div[2]/div/div[5]/article["+str(i)+"]/div/a[1]/h2"
            LOGGER.info("Clicking on product")
            time.sleep(2)
            driver.find_element_by_xpath(xpath).click()
            select_properties(driver)
            counter += 1
            if counter == 15:
                time.sleep(2)
                click_next(driver)
    elif click_next_counter > 13:
        return
    # xpath_1 = "//*[@id='product-family-page']/section[3]/div/div[2]/div/div[5]/article[15]/div/a[1]/h2"
    # LOGGER.info("Clicking on product")
    # driver.find_element_by_xpath(xpath_1).click()
    # ActionChains(driver).move_to_element(link).click().perform()
    return



def click_next(driver):
    #Function for clicking on the next button.
    global click_next_counter
    click_next_counter += 1
    driver.execute_script("window.scrollTo(0, 600)")
    time.sleep(3)
    #The Xpath of the next button changes based on the page. Hence, different Xpaths are assigned.
    if click_next_counter < 4:
        xpath = "//*[@id='product-family-page']/section[3]/div/div[2]/div/div[4]/div/div/ul/li[7]/a"
    elif click_next_counter >3 and click_next_counter < 10:
        xpath = "//*[@id='product-family-page']/section[3]/div/div[2]/div/div[4]/div/div/ul/li[9]/a"
    elif click_next_counter > 9 and click_next_counter < 14:
        xpath = "//*[@id='product-family-page']/section[3]/div/div[2]/div/div[4]/div/div/ul/li[8]/a"
    elif click_next_counter > 13:
        return
    LOGGER.info("Clicking next")
    driver.find_element_by_xpath(xpath).click()
    open_product(driver)
    # xpath_1 = "//*[@id='product-family-page']/section[3]/div/div[2]/div/div[5]/article[15]/div/a[1]/h2"
    # time.sleep(2)
    # driver.find_element_by_xpath(xpath).click()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--driver-type", default="chrome", choices=("firefox", "chrome"))
    args = parser.parse_args()

    #Set driver properties based on Operating systems and Browser types.

    driver = None
    if args.driver_type == "firefox":
        options = webdriver.FirefoxOptions()
        # if args.headless:
        #     options.add_argument("--headless")
        executable_path = None
        if sys.platform == "darwin":
            executable_path = "./bin/geckodriver_mac"
        elif "linux" in sys.platform:
            executable_path = "./bin/geckodriver_linux"
        driver = webdriver.Firefox(executable_path=executable_path, firefox_options=options, log_path=os.devnull)
    elif args.driver_type == "chrome":
        options = webdriver.ChromeOptions()
        # if args.headless:
        #     options.add_argument("headless")
        executable_path = None
        if sys.platform == "darwin":
            executable_path = "./bin/chromedriver_mac"
        elif "linux" in sys.platform:
            executable_path = "./bin/chromedriver_linux"
        driver = webdriver.Chrome(executable_path=executable_path, chrome_options=webdriver.ChromeOptions())
    run(driver=driver)
