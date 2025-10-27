from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time
import geckodriver 
"""
Hiermit wird adminer in einem neuen TAB gestartet und nachdem kurz der TAB gezeigt wurde,
wird wieder die Hauptseite angezeigt.

Args:
driver ist eine globale Variable die durch den geckodriver import bereitgestellt wird und
die dann sowohl den Firefox-Browser als auch die Webseite startet. 
"""

def adminer_view():
    if geckodriver.driver is None:
        raise Exception("Browser wurde nicht gestartet. Bitte zuerst start_browser() aufrufen.")
    
    geckodriver.driver.execute_script("window.open('http://localhost:8080', '_blank');")
    geckodriver.driver.switch_to.window(geckodriver.driver.window_handles[-1])
    #time.sleep(4)
    #geckodriver.driver.switch_to.window(geckodriver.driver.window_handles[0])
