
from selenium import webdriver
from geckodriver import start_browser
from trim_log import trim_robot_log
from docker_control import start_docker

driver = webdriver.Firefox()
driver.get("https://www.saucedemo.com")





if __name__ == 'main':
    start_browser()
    start_docker()
    
    trim_robot_log()