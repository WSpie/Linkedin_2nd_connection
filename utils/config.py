import os
import yaml
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.core.os_manager import ChromeType
from webdriver_manager.chrome import ChromeDriverManager

from pathlib import Path

class Namespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

def load_config(config_path):
    config = yaml.safe_load(Path(config_path).read_text())
    return Namespace(**config)

def config_options(options, headless):
    options.add_argument('--no-sandbox')
    options.add_argument('--incognito')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--start-maximized')
    options.add_argument('--disable-webgl')
    options.add_argument('--log-filter=-*WebGL*')  # Filter out WebGL-related messages
    options.add_argument('--disable-features=WebRtcHideLocalIpsWithMdns')
    options.add_argument('--disable-gpu')
    options.add_argument('--log-level=3')  # Suppresses most log messages
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_experimental_option("useAutomationExtension", False)  # Adding Argument to Not Use Automation Extension
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Excluding enable-automation Switch
    options.add_argument("disable-popup-blocking")
    if headless:
        options.add_argument('--headless')
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    options.add_experimental_option("prefs", prefs)
    return options

def init_driver(config_path, headless=False):
    config = load_config(config_path)
    options = config_options(webdriver.ChromeOptions(), headless)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install(), service_log_path=os.devnull), options=options)
    return driver, config




