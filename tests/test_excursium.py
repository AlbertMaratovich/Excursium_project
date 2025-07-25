from pages.excursion_page import ExcursionPage
from pages.login_page import LoginPage
from pages.main_page import MainPage
from config import config
import pytest
import allure
import time


@allure.feature("Пользовательские сценарии")
class TestUserCases:

    @allure.title("Авторизация в аккаунт с корректными данными")
    @allure.severity("Critical")
    @pytest.mark.auth
    def test_enter_account_correct_data(self, driver):
        """Проверка возможности входа в аккаунт с корректными данными"""
        with allure.step("Открываем страницу"):
            login_page = LoginPage(driver)
            driver.get(config.base_url)

        with allure.step("Переходим к странице логина"):
            driver.find_element(*login_page.login_header).click()
            assert login_page.is_opened(config.login_url), "Отсутствует переход к страница логина"

        with allure.step("Вводим имейл"):
            field_email = driver.find_element(*login_page.field_email)
            field_email.clear()
            field_email.send_keys(config.login)

        with allure.step("Вводим пароль"):
            password_field = driver.find_element(*login_page.password_field)
            password_field.clear()
            password_field.send_keys(config.password)

        with allure.step("Кликаем на кнопку логина в аккаунт"):
            driver.find_element(*login_page.login_btn).click()
            assert login_page.is_opened(config.account_url), "Не произошел вход в аккаунт"

    @allure.title("Оформление экскурсии")
    @allure.severity("Critical")
    @pytest.mark.user_case
    def test_order_excursion(self, driver):
        """Переход с главной страницы к экскурсиям с дальнейшим оформлением одной из них (юзер-сценарий)"""
        excursion_page = ExcursionPage(driver)
        main_page = MainPage(driver)

        with allure.step("Открываем страницу"):
            driver.get(config.base_url)

        with allure.step("Переходим на страницу с экскурсиями"):
            driver.find_element(*main_page.all_excursion_btn).click()

        with allure.step("Переходим на страницу первой экскурсии списка"):
            first_excursion = main_page.excursions()[0]
            first_excursion.click()

        # change the handle
        excursion_page.move_last_handle()
        page_url = driver.current_url

        # scroll to order button and click
        order_button = driver.find_element(*excursion_page.order_button)
        excursion_page.scroll_to(order_button)

        with allure.step("Кликаем на кнопку заказа"):
            order_button.click()

        with allure.step("Ждем и проверяем открытие окна"):
            order_window = driver.find_element(*excursion_page.order_window)
            main_page.wait.until(lambda x: order_window.is_displayed())

        with (allure.step("Заполняем поля корректными данными")):
            driver.find_element(*excursion_page.date_field).click()
            first_day = driver.find_elements("xpath", "//div/span[@class='flatpickr-day ']")[0]
            main_page.is_clickable(first_day)
            first_day.click()
            name_field = driver.find_element(*excursion_page.name_field)
            name_field.send_keys("Это Автотест")
            phone_field = driver.find_element(*excursion_page.phone_field)
            phone_field.send_keys("9999999999")
            excursion_page.check_box()

        with allure.step("Проверяем кликабельность кнопки после заполнения формы"):
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

    @allure.title("Переход на страницу с жалобами")
    @allure.severity("Normal")
    @pytest.mark.user_case
    def test_user_report_problem(self, driver):
        """Пользовательский сценарий перехода на вкладку с экскурсиями и на страницу с жалобами"""
        main_page = MainPage(driver)

        with allure.step("Открываем страницу"):
            driver.get(config.base_url)

        with allure.step("Переходим на страницу с экскурсиями"):
            driver.find_element(*main_page.all_excursion_btn).click()

        with allure.step("Находим и скролим до кнопки отправки жалобы"):
            report_btn = driver.find_element(*main_page.report_btn)
            main_page.scroll_to(report_btn)
            main_page.is_clickable(report_btn)
            report_btn.click()

        assert driver.current_url == config.feedback_url, "URL не соответствует странице отправки фидбека"
