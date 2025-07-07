from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(driver)
        self.wait = WebDriverWait(driver, 10)

    def is_opened(self, page: str):
        page = page
        return self.wait.until(EC.url_to_be(page))

    def is_clickable(self, element):
        if element.is_displayed() and element.is_enabled():
            return True
        else:
            return False

    def move_last_handle(self):
        tabs = self.driver.window_handles
        self.driver.switch_to.window(tabs[-1])

    def scroll_to(self, element):
        self.actions.scroll_to_element(element).perform()
        self.driver.execute_script("""window.scrollTo({top: window.scrollY + 500,});""")

    def scroll_down(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_top(self):
        self.driver.execute_script("window.scrollTo(0, 0)")
