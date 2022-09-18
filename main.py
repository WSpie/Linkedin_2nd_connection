from selenium import webdriver
import os
import time
from bs4 import BeautifulSoup
import re
import sys
import yaml
from pathlib import Path
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import warnings
warnings.filterwarnings('ignore')

class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def load_config():
    config = yaml.safe_load(Path('cfg.yaml').read_text())
    return Namespace(**config)

config = load_config()
username = config.username
password = config.password
school = config.school


chrome_driver_path = os.path.join('widget', 'chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument('--start-maximized')
options.add_argument('--disable-gpu')
options.add_experimental_option("useAutomationExtension", False)  # Adding Argument to Not Use Automation Extension
options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Excluding enable-automation Switch
options.add_argument("disable-popup-blocking")
# options.add_argument('--headless')
prefs = {"profile.default_content_setting_values.notifications" : 2}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_driver_path, options=options)

login_url = 'https://www.linkedin.com/login'
connection_url = 'https://www.linkedin.com/mynetwork/invite-connect/connections/'

# login
driver.get(login_url)
driver.implicitly_wait(10)
driver.find_element_by_xpath('//*[@id="username"]').send_keys(username)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button').click()
driver.implicitly_wait(10)
# check if succeeed
try:
    driver.find_element_by_css_selector('div.feed-identity-module__member-bg-image')
    print('Easy login')
except:
    print('Need further step')
    time.sleep(5)
    # print(driver.find_element_by_xpath('//*[@id="home_children_heading"]').text)
    
    driver.implicitly_wait(10)
    sys.exit(0)

# select 2nd connection
driver.get(connection_url)
driver.implicitly_wait(10)
driver.find_element_by_css_selector('a.ember-view').click()
driver.implicitly_wait(10)
driver.find_element_by_css_selector('button[class^=artdeco-pill]').click()
driver.implicitly_wait(10)
driver.find_element_by_xpath('//span[text()="1st"]').click()
driver.implicitly_wait(10)
driver.find_element_by_xpath('//span[text()="2nd"]').click()
driver.implicitly_wait(10)
driver.find_element_by_xpath('//span[text()="Show results"]').click()
driver.implicitly_wait(10)
# filter and check
driver.refresh()
driver.implicitly_wait(10)
# people_p1_url = '&'.join(driver.current_url.split('&')[:-1])
people_p1_url = 'https://www.linkedin.com/search/results/people/?network=%5B%22S%22%5D&origin=FACETED_SEARCH'
sid = driver.current_url.split('&')[-1]
driver.get(people_p1_url)

page = 1
while True:
    driver.implicitly_wait(10)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    people_blks = soup.select('ul.reusable-search__entity-result-list li')
    blks_num = len(people_blks)
    for blk in range(blks_num):
        # only open the url 'Connect' available
        status = people_blks[blk].select('span.artdeco-button__text')[0].text
        status = status.replace('\n', '').replace(' ', '')
        if status != 'Connect':
            continue
        person_url = people_blks[blk].select('a.app-aware-link')[0]['href']
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        
        # open personal page
        driver.get(person_url)
        driver.implicitly_wait(20)
        
        # get first name or preferred name
        person_soup = BeautifulSoup(driver.page_source, 'html.parser')
        full_name = person_soup.select('h1.text-heading-xlarge')[0].text
        try:
            name = re.findall('\((.*?)\)', full_name)[0]
        except:
            name = full_name.split(' ')[0]
        # print(name)
        
        # filter alumni by highlights
        sections = person_soup.select('section.artdeco-card')
        section_idx = None
        for idx, section in enumerate(sections):
            if section.select('div#highlights'):
                section_idx = idx
                break
        
        # check highlights
        person_type = 'Stranger'
        if section_idx:
            section = sections[section_idx]
            highlights_blks = section.select('li.artdeco-list__item')
            for highlights_blk in highlights_blks:
                highlights_content = highlights_blk.select('span.visually-hidden')[0].text
                if school in highlights_content:
                    person_type = 'Alumni'
                    break
        print(f'{name}: {person_type}')
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    
    page += 1
    next_page_url = people_p1_url + f'&page={page}&{sid}'
    try:
        driver.get(next_page_url)
    except:
        break

time.sleep(20)
driver.close()
driver.quit()
    

