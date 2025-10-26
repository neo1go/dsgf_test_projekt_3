from selenium import webdriver
import time
driver = webdriver.Firefox()

try:
    driver.get("https://www.saucedemo.com")
    print(driver.title)
    time.sleep(10)
finally:
    driver.quit()