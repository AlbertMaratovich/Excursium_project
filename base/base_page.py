from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import allure


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(driver)
        self.wait = WebDriverWait(driver, 10)

    def is_opened(self, page: str):
        with allure.step("Проверяем открыта ли страница"):
            page = page
            return self.wait.until(EC.url_to_be(page))

    def is_clickable(self, element):
        with allure.step("Проверяем кликабелен ли элемент"):
            if element.is_displayed() and element.is_enabled():
                return True
            else:
                return False

    def move_last_handle(self):
        with allure.step("Переходим на открытую вкладку"):
            tabs = self.driver.window_handles
            self.driver.switch_to.window(tabs[-1])

    def scroll_to(self, element):
        with allure.step("Скроллим до элемента"):
            self.actions.scroll_to_element(element).perform()
            self.driver.execute_script("window.scrollBy(0, 500);")
            # self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def scroll_down(self):
        with allure.step("Скроллим вниз страницы"):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_top(self):
        with allure.step("Скроллим вверх страницы"):
            self.driver.execute_script("window.scrollTo(0, 0)")
