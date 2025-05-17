from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os

def setup_driver():
    chrome_path = os.path.join(os.path.dirname(__file__), 'chromedriver.exe')
    service = Service(executable_path=chrome_path)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver
