from bs4 import BeautifulSoup
import sys
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import threading

def random_scroll(driver):
    seg = 100
    height = driver.execute_script("return document.body.scrollHeight")
    scroll_choice = [f"window.scrollTo(0,{int(i*seg)})" for i in range(height//10 - 1)]
    scroll_move_list = random.choices(scroll_choice, weights=[100/len(scroll_choice)]*len(scroll_choice), k=random.randint(1, 5))
    # print(scroll_move_list)
    for scroll_move in scroll_move_list:
        driver.execute_script(scroll_move)
        time.sleep(random.random())
    return driver

class TimeoutException(Exception):
    pass

def timeout(seconds):
    def decorator(func):
        def wrapper(*args, **kwargs):
            def inner():
                try:
                    result[0] = func(*args, **kwargs)
                except Exception as e:
                    result[0] = e

            result = [None]
            thread = threading.Thread(target=inner)
            thread.start()
            thread.join(seconds)
            if thread.is_alive():
                raise TimeoutException(f"Function {func.__name__} timed out after {seconds} seconds")
            if isinstance(result[0], Exception):
                raise result[0]
            return result[0]
        return wrapper
    return decorator

@timeout(30)
def connect_with_alumni(driver, name, full_name, greeting_txt_path, config, logger, sent_request_cnt, total_requests):
    try:
        notes = ''
        with open(greeting_txt_path, 'r') as f:
            notes = ''.join(f.readlines())
        notes = notes.replace('?name?', name).replace('?school?', config.school)
        connect_btn = driver.find_element(By.XPATH, '//button[span[text()="Connect"]]')
        driver.execute_script('arguments[0].click();', connect_btn)
        time.sleep(random.randint(1, 2))
        add_note_btn = driver.find_element(By.XPATH, '//span[text()="Add a note"]')
        driver.execute_script('arguments[0].click();', add_note_btn)
        time.sleep(random.randint(1, 2))
        driver.find_element(By.XPATH, '//*[@id="custom-message"]').send_keys(notes)
        time.sleep(random.randint(1, 2))
        driver.implicitly_wait(10)
        send_btn = driver.find_element(By.XPATH, '//span[text()="Send"]')
        driver.execute_script('arguments[0].click()', send_btn)
        driver.implicitly_wait(10)
        sent_request_cnt += 1
        logger.record(full_name, sent_request_cnt, total_requests)
    except:
        if driver.find_element(By.CSS_SELECTOR, 'h2.upsell-modal-header').text == 'No free personalized invitations left':
            logger.no_free_connections()
            sys.exit(0)
    return sent_request_cnt


def request_and_next_page(driver, config, logger, total_requests, greeting_txt_path):
    sent_request_cnt = 0
    driver.implicitly_wait(10)
    page = 1
    done_flag = False
    while True:
        try:
            # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            # driver.implicitly_wait(10)
            # driver.execute_script("window.scrollTo(0,0)")
            time.sleep(random.randint(1, 2))
            # soup = BeautifulSoup(driver.page_source, 'html.parser')
            # people_blks = soup.select('ul.reusable-search__entity-result-list li.reusable-search__result-container')
            # blks_num = len(people_blks)
            people_blks = driver.find_elements(By.CSS_SELECTOR, 'li.reusable-search__result-container')
            blks_num = len(people_blks)
            for blk in range(blks_num):
                # only open the url 'Connect' available
                # status = people_blks[blk].find_element_by_css_selector('span.artdeco-button__text').text
                status = people_blks[blk].find_element(By.CSS_SELECTOR, 'span.artdeco-button__text').text
                # status = people_blks[blk].select('button.artdeco-button span.artdeco-button__text')[0].text
                # status = status.replace('\n', '').replace(' ', '')
                if status != 'Connect':
                    continue
                # person_url = people_blks[blk].select('a.app-aware-link')[0]['href']
                # person_url = people_blks[blk].find_element_by_css_selector('a.app-aware-link').get_attribute('href')
                person_url = people_blks[blk].find_element(By.CSS_SELECTOR, 'a.app-aware-link').get_attribute('href')
                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[1])
                
                # open personal page
                driver.get(person_url)
                driver.implicitly_wait(20)
                driver = random_scroll(driver)
                time.sleep(random.randint(1, 2))
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
                        if config.school in highlights_content:
                            person_type = 'Alumni'
                            break
                
                # send connection invitation to alumni with greetings
                if person_type == 'Alumni':
                    try:
                        sent_request_cnt = connect_with_alumni(driver, name, full_name, greeting_txt_path, config, logger, sent_request_cnt, total_requests)
                        if sent_request_cnt >= total_requests:
                            done_flag = True
                            break
                    except TimeoutException as e:
                        print(f"Timeout occurred: {e}")
                    except Exception as e:
                        logger.unable_connect(name, e)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
        except:
            logger.unable_parse_page(page)
        if done_flag:
            break
        page += 1
        try:
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            driver.implicitly_wait(10)
            # next_btn = driver.find_element_by_xpath('//span[text()="Next"]')
            next_btn = driver.find_element(By.XPATH, '//span[text()="Next"]')
            driver.execute_script('arguments[0].click()', next_btn)
        except:
            logger.no_next_page(page)
            break
    logger.msg(f'Sent {sent_request_cnt} connection invitations! Job Done!')
    return driver