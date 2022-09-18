from selenium import webdriver
import os
import time
from bs4 import BeautifulSoup
import re
import sys
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from utils.logger import Log
from utils.config import init_driver
from utils.login import login
from utils.second_connection import sec_conn
from utils.send_request import request_and_next_page

import warnings
warnings.filterwarnings('ignore')

if __name__ == '__main__':
    # conifgurate driver and load user info
    driver, config = init_driver()
    # login
    driver = login(driver, config)
    # auto choose 2nd connection and go page 1
    driver = sec_conn(driver)
    # send request to alumni and next page
    logger = Log(config)
    driver = request_and_next_page(driver, config, logger)
    
    driver.quit()
    
    
    
    

