from base.base_page import BasePage
import allure


class ExcursionPage(BasePage):
    order_button = ("xpath", "//div/button[@aria-label='Заказать экскурсию для школьников']")
    order_window = ("id", "bookingModal")
    date_field = ("id", "bookingDates")
    name_field = ("id", "bookingUserName")
    phone_field = ("id", "orderPhone")
    send_order_btn = ("xpath", "//div/button[@aria-label='Отправить заявку']")
    success_window = ("id", "bookingSuccess")
    good_btn = ("xpath", "//div/button[contains(text(), ' Хорошо ')]")
    size_25_34 = ("xpath", "//label[contains(text(), ' 25–34 ')]")

    def check_box(self):
        with allure.step("Установка/снятие чекбокса"):
            check_box = self.driver.find_element("id", "agreeCheck")
            check_box.click()
