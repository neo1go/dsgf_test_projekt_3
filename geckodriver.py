    
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

def start_browser():
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    driver.get("https://www.saucedemo.com")
    print(driver.title)
    return driver