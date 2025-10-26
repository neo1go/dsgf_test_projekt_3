
from selenium import webdriver
from geckodriver import start_browser
from trim_log import trim_robot_log

driver = webdriver.Firefox()
driver.get("https://www.saucedemo.com")





if __name__ == 'main':
    start_browser()
    
    trim_robot_log()