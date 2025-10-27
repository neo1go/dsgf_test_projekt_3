from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

driver = None  # global definiert

def start_browser():
    global driver
    service = Service(GeckoDriverManager().install())
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(service=service, options=options)
    driver.get("https://www.saucedemo.com")
    return driver
