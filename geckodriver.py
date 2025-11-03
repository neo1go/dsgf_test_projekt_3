from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import os
# globaler Driver
driver = None

def start_browser():
    """
    Startet den Firefox-Browser (sichtbar) und initialisiert die globale driver-Variable.
    Verwendet einen festen Pfad zum Geckodriver.
    """
    global driver

    # Fester Pfad zum Geckodriver
    geckodriver_path = r"C:\Users\Willkommen\.wdm\drivers\geckodriver\win64\v0.36.0\geckodriver.exe"

    # Firefox-Optionen (sichtbar, nicht headless)
    options = Options()
    options.headless = False
    
    log_file_path = os.path.join("results", "geckodriver.log")
    
   # Selenium-WebDriver Service mit reduziertem Log-Level
    service = Service(
        executable_path=geckodriver_path,
        log_output = log_file_path,
        log_level = "error"  # Alternativen: error, all, debug, info, warning, severe, off oder eventuell os.devnull
    )

    # Firefox WebDriver starten
    driver = webdriver.Firefox(service=service, options=options)

    # Startseite öffnen
    driver.get("https://www.saucedemo.com")

    return driver
