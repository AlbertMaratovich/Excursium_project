from pages.excursion_page import ExcursionPage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from selenium.webdriver.support.ui import WebDriverWait
from config import config
import time


class TestUserCases:
    def test_enter_account_correct_data(self, driver):
        """Проверка возможности входа в аккаунт с корректными данными"""
        login_page = LoginPage(driver)
        driver.get(config.base_url)

        # move to login page
        driver.find_element(*login_page.login_header).click()
        assert login_page.is_opened(config.login_url), "Отсутствует переход к страница логина"

        # enter an email to the field
        field_email = driver.find_element(*login_page.field_email)
        field_email.clear()
        field_email.send_keys(config.login)

        # enter a password to the field
        password_field = driver.find_element(*login_page.password_field)
        password_field.clear()
        password_field.send_keys(config.password)

        # click on a login button
        driver.find_element(*login_page.login_btn).click()
        assert login_page.is_opened(config.account_url), "Не произошел вход в аккаунт"

    def test_order_excursion(self, driver):
        """Переход с главной страницы к экскурсиям с дальнейшим оформлением одной из них (юзер-сценарий)"""
        excursion_page = ExcursionPage(driver)
        main_page = MainPage(driver)
        driver.get(config.base_url)

        # click on all excursion button
        driver.find_element(*main_page.all_excursion_btn).click()

        # click on first excursion
        first_subject = driver.find_elements("xpath", "//div[@class='col']/div/div")[0]
        first_subject.click()

        # change the handle
        excursion_page.move_last_handle()
        page_url = driver.current_url

        # scroll to order button and click
        order_button = driver.find_element(*excursion_page.order_button)
        excursion_page.scroll_to(order_button)
        order_button.click()

        # check the order window is displayed
        order_window = driver.find_element(*excursion_page.order_window)
        WebDriverWait(driver, 5).until(lambda x: order_window.is_displayed())

        # add data to fields
        driver.find_element(*excursion_page.date_field).click()
        driver.find_elements("xpath", "//div/span[@class='flatpickr-day ']")[0].click()
        name_field = driver.find_element(*excursion_page.name_field)
        name_field.send_keys("Это Автотест")
        phone_field = driver.find_element(*excursion_page.phone_field)
        phone_field.send_keys("9999999999")
        excursion_page.check_box()

        # send order
        send_order_btn = driver.find_element(*excursion_page.send_order_btn)
        assert excursion_page.is_clickable(send_order_btn), "Кнопка не кликабельна после заполнения формы"

        """use below strings in dev environment"""
    # click on send order button
        # send_order_btn.click()
        # success_window = driver.find_element(*excursion_page.success_window)
        # assert success_window.is_displayed(), "Окно успешной отправки заявки не отобразилось"
        # driver.find_element(*excursion_page.good_btn").click()
        # assert not success_window.is_displayed(), "Окно успешной отправки заявки отображается после закрытия кнопкой"
        # assert driver.current_url == page_url, "URL не соответствует странице экскурсии"

    def test_user_report_problem(self, driver):
        """Пользовательский сценарий перехода на вкладку с экскурсиями и на страницу с жалобами"""
        main_page = MainPage(driver)
        driver.get(config.base_url)

        # move to all excursion page
        driver.find_element(*main_page.all_excursion_btn).click()

        # click on report button
        report_btn = driver.find_element(*main_page.report_btn)
        main_page.scroll_to(report_btn)
        report_btn.click()

        # check the url
        assert driver.current_url == config.feedback_url, "URL не соответствует странице отправки фидбека"
