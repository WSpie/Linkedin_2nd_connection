import time
import random
from selenium.webdriver.common.by import By

connection_url = 'https://www.linkedin.com/mynetwork/invite-connect/connections/'

def sec_conn(driver):
# select 2nd connection
    driver.get(connection_url)
    driver.implicitly_wait(10)
    time.sleep(random.randint(1, 3))
    # driver.find_element_by_css_selector('a.ember-view').click()
    driver.find_element(By.CSS_SELECTOR, 'a.ember-view').click()
    driver.implicitly_wait(10)
    # driver.find_element_by_css_selector('button[class^=artdeco-pill]').click()
    driver.find_element(By.CSS_SELECTOR, 'button[class^=artdeco-pill]').click()
    driver.implicitly_wait(10)
    time.sleep(random.randint(1, 2))
    # driver.find_element_by_xpath('//span[text()="1st"]').click()
    driver.find_element(By.XPATH, '//span[text()="1st"]').click()
    driver.implicitly_wait(10)
    time.sleep(random.randint(1, 2))
    # driver.find_element_by_xpath('//span[text()="2nd"]').click()
    driver.find_element(By.XPATH, '//span[text()="2nd"]').click()
    driver.implicitly_wait(10)
    time.sleep(1)
    # driver.find_element_by_xpath('//span[text()="Show results"]').click()
    driver.find_element(By.XPATH, '//span[text()="Show results"]').click()
    driver.implicitly_wait(10)
    return driver
    