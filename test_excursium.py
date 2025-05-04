from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from config import base_url, login, password
import time

driver = webdriver.Chrome()
driver.get(base_url)
driver.set_window_size(1920, 1080)


def test_enter_account_correct_data():
    """Проверка возможности входа в аккаунт с корректными данными"""
    driver.implicitly_wait(10)
    login_button = driver.find_element("xpath", "//li/a[@data-bs-original-title='Войти']")
    login_button.click()

    if driver.current_url != "https://excursium.com/Client/Login":
        raise Exception("URL не соответствует ожидаемому")

    # enter an email to the field
    field_email = driver.find_element("xpath", "//form/div/input[@type='email']")
    field_email.clear()
    field_email.send_keys(login)

    # enter an email to the field
    field_password = driver.find_element("xpath", "//div/form/div[2]/input[@class='form-control fakepassword']")
    field_password.clear()
    field_password.send_keys(password)

    # click on a login button
    driver.find_element("id", "login-btn").click()
    time.sleep(0.5)

    assert driver.current_url == "https://excursium.com/Account/Startup"


def test_users_path_1():
    """Пользовательский сценарий поиска на странице экскурсии, перехода к её карточке и переход в ТГ для связи"""
    driver.get(base_url)

    # click on all excursion button
    driver.find_element("xpath", "//div/ul/li/a[contains(text(), 'Все экскурсии')]").click()

    # click on excursion
    first_subject = driver.find_element("xpath", "//div[@class='col']/div/div")
    first_subject.click()

    # change the handle
    tabs = driver.window_handles
    driver.switch_to.window(tabs[-1])

    tg_button = driver.find_element("xpath", "//div/button[@onclick='Helpers.writeToTelegram()']")

    # scroll to button and click
    ActionChains(driver).move_to_element(tg_button).click().perform()

    # change the handle
    tabs = driver.window_handles
    driver.switch_to.window(tabs[-1])

    # check the url
    assert "https://t.me/excursium" in driver.current_url


def test_user_report_problem():
    """Пользовательский сценарий перехода на вкладку с экскурсиями и на страницу с жалобами"""
    driver.get(base_url)

    # click on all excursion button
    driver.find_element("xpath", "//div/ul/li/a[contains(text(), 'Все экскурсии')]").click()

    report_button = driver.find_element("xpath", "//div/p/a[@href='/About/Contact#from-feedback']")

    # scroll to button
    action = ActionChains(driver).scroll_to_element(report_button)
    action.perform()
    time.sleep(1)

    # доскролить пришлось, а то кликалось мимо)
    html = driver.find_element("tag name", "html")
    for i in range(10):
        html.send_keys(Keys.ARROW_DOWN)
    time.sleep(0.3)

    # click on a report button
    action.click(report_button).perform()

    # check the url
    assert driver.current_url == "https://excursium.com/About/Contact#from-feedback"
