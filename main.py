
from selenium import webdriver
from geckodriver import start_browser
from trim_log import trim_geckodriver_log
from docker_control import start_containers
from docker_control import stop_containers
from docker_control import remove_containers
from docker_desktop_start import docker_app_start
from adminer_interface import adminer_view
from robot_start import start_robot_tests
from show_log_html import show_log_in_browser, start_webserver, stop_webserver
import time

def main():
    try:
        start_browser()
        docker_app_start()
        time.sleep(20)
        start_containers()
        time.sleep(15)
        adminer_view()
        start_webserver()
        show_log_in_browser()
        stop_webserver()
        start_robot_tests()
    except Exception as e:
        print(f"Fehler im Ablauf: {e}")
        
    #stop_containers()
    #remove_containers()
    # trim_geckodriver_log()



if __name__ == '__main__':
    main()