import os
import sys
import requests
from selenium.webdriver.common.keys import Keys
import time
import argparse
import logging.config
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from dateutil import parser as date_parser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

"""

This is an experimental script which attempts at utilizing some Nike APIs.

Current implementation:
    1. Login with Selenium
    2. Using the driver's stored cookies, make a Nike API request to add the desired item to your cart
    3. Load the checkout page and place an order
    
Not sure if this will be any faster than the other script...

"""


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
    driver.execute_script("window.history.go(-1)")
    time.sleep(2)
    return

def open_product(driver):
    time.sleep(2)
    counter = 0
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
    # xpath_1 = "//*[@id='product-family-page']/section[3]/div/div[2]/div/div[5]/article[15]/div/a[1]/h2"
    if counter == 15:
        time.sleep(2)
        click_next(driver)
    # LOGGER.info("Clicking on product")
    # driver.find_element_by_xpath(xpath_1).click()
    # ActionChains(driver).move_to_element(link).click().perform()
    return



def click_next(driver):
    driver.execute_script("window.scrollTo(0, 600)")
    time.sleep(2)
    xpath = "//*[@id='product-family-page']/section[3]/div/div[2]/div/div[4]/div/div/ul/li[7]/a"
    LOGGER.info("Clicking next")
    driver.find_element_by_xpath(xpath).click()
    open_product(driver)
    # xpath_1 = "//*[@id='product-family-page']/section[3]/div/div[2]/div/div[5]/article[15]/div/a[1]/h2"
    # time.sleep(2)
    # driver.find_element_by_xpath(xpath).click()
    return



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--driver-type", default="chrome", choices=("firefox", "chrome"))
    args = parser.parse_args()

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
