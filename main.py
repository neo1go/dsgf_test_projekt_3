
from selenium import webdriver
from geckodriver import start_browser
from trim_log import trim_robot_log
from docker_control import start_containers
from docker_control import stop_containers
from docker_control import remove_containers
from docker_desktop_start import docker_app_start
from adminer_interface import adminer_view

def main():
    start_browser()
    docker_app_start()
    start_containers()
    adminer_view()
    # Seite mit selenium scrappen
    # Tests an den Daten ausführen
    # Daten in die Datenbank schreiben
  
    
    #stop_containers()
    #remove_containers()
    trim_robot_log()



if __name__ == '__main__':
    main()