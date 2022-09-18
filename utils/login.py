import time, sys
login_url = 'https://www.linkedin.com/login'

def login(driver, config):
    driver.get(login_url)
    driver.implicitly_wait(10)
    driver.find_element_by_xpath('//*[@id="username"]').send_keys(config.username)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys(config.password)
    driver.find_element_by_xpath('//*[@id="organic-div"]/form/div[3]/button').click()
    driver.implicitly_wait(10)
    # check if succeeed
    try:
        driver.find_element_by_css_selector('div.feed-identity-module__member-bg-image')
        print('Easy login')
    except:
        # !!!!!
        # will finalize in next version
        print('Need further step')
        time.sleep(5)
        # print(driver.find_element_by_xpath('//*[@id="home_children_heading"]').text)
        driver.implicitly_wait(10)
        sys.exit(0)
    return driver