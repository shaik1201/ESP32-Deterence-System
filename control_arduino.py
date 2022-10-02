# import module
from selenium import webdriver
import time

def func(led_state):


    # Create the webdriver object. Here the
    # chromedriver is present in the driver
    # folder of the root directory.
    driver = webdriver.Edge(r"C:/Users/shaik/Downloads/edgedriver_win32/msedgedriver.exe")

   
    driver.get("http://192.168.1.30/")

    # Maximize the window and let code stall
    # for 10s to properly maximise the window.
    driver.maximize_window()
    time.sleep(5)

    # Obtain button by link text and click.
    button = driver.find_element("link text", led_state)
    button.click()
