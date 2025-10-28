
from selenium import webdriver
from geckodriver import start_browser
from trim_log import trim_robot_log
from docker_control import start_containers
from docker_control import stop_containers
from docker_control import remove_containers
from docker_desktop_start import docker_app_start
from adminer_interface import adminer_view
from robot_start import start_robot_tests
import time

def main():
    start_browser()
    docker_app_start()
    time.sleep(20)
    start_containers()
    time.sleep(20)
    adminer_view()
    time.sleep(10)
    start_robot_tests()
  
    
    #stop_containers()
    #remove_containers()
    trim_robot_log()



if __name__ == '__main__':
    main()