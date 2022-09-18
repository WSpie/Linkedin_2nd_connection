import os
import yaml
from selenium import webdriver
from pathlib import Path

class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def load_config():
    config = yaml.safe_load(Path('cfg.yaml').read_text())
    return Namespace(**config)

def init_driver():
    config = load_config()
    chrome_driver_path = os.path.join('widget', 'chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-gpu')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("useAutomationExtension", False)  # Adding Argument to Not Use Automation Extension
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Excluding enable-automation Switch
    options.add_argument("disable-popup-blocking")
    # options.add_argument('--headless')
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)
    return driver, config




