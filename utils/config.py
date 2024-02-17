import os
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.core.os_manager import ChromeType
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.ie.service import Service as IEService
from webdriver_manager.microsoft import IEDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.service import Service as BraveService

from pathlib import Path

class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def load_config(config_path):
    config = yaml.safe_load(Path(config_path).read_text())
    return Namespace(**config)

def init_driver(driver_name, config_path, headless=False):
    config = load_config(config_path)
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-gpu')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("useAutomationExtension", False)  # Adding Argument to Not Use Automation Extension
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Excluding enable-automation Switch
    options.add_argument("disable-popup-blocking")
    if headless:
        options.add_argument('--headless')
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs", prefs)
    if driver_name == 'chrome':
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    elif driver_name == 'chromium':
        driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)
    elif driver_name == 'brave':
        driver = webdriver.Chrome(service=BraveService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()), options=options)
    elif driver_name == 'edge':
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
    elif driver_name == 'firefox':
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    else: # ie
        driver = webdriver.Ie(service=IEService(IEDriverManager().install()), options=options)
        
    return driver, config




