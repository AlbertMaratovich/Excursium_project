from selenium import webdriver
from config import base_url, login, password

driver = webdriver.Chrome()
driver.get(base_url)
driver.set_window_size(1920, 1080)


def test_somthing():
    return None
