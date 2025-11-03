#from selenium import webdriver
from selenium.webdriver.firefox.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager 
import geckodriver 
import json

""" 
Hiermit wird adminer in einem neuen TAB gestartet.
 
Args: 
driver ist eine globale Variable die durch den geckodriver import 
bereitgestellt wird und die dann sowohl den Firefox-Browser als auch die Webseite startet. 
""" 
# Credentials werden aus der config ausgelesen:
with open("config/config.json", "r") as file:
    config = json.load(file)

# Variablenbelegung aus der json.config
adminer_config = config["adminer"]
driver_type = adminer_config["Driver"]
server = adminer_config["Server"]
user = adminer_config["Benutzer"]
password = adminer_config["Passwort"]
database = adminer_config["Datenbank"]
 
#Adminer Aufruf in neuem TAB
def adminer_view(): 
    if geckodriver.driver is None: 
        raise Exception("Browser wurde nicht gestartet. Bitte zuerst start_browser() aufrufen.") 
    geckodriver.driver.execute_script("window.open('http://localhost:8080', '_blank');") 
    
    geckodriver.driver.switch_to.window(geckodriver.driver.window_handles[-1])
    
    wait = WebDriverWait(geckodriver.driver, 10)
    
    #löscht den vorherigen Eintrag
    db_field = wait.until(EC.presence_of_element_located((By.NAME, "auth[server]")))
    db_field.clear()

    # relevante Felder befüllen, sobald sie geladen wurden.
    wait.until(EC.presence_of_element_located((By.NAME, "auth[server]"))).send_keys(server)
    wait.until(EC.presence_of_element_located((By.NAME, "auth[username]"))).send_keys(user)
    wait.until(EC.presence_of_element_located((By.NAME, "auth[password]"))).send_keys(password)
    wait.until(EC.presence_of_element_located((By.NAME, "auth[db]"))).send_keys(database)

    #  Login-Button klicken
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Login']"))).click()