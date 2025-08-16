from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import allure
import time


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(driver)
        self.wait = WebDriverWait(driver, 10)

    def is_opened(self, page: str) -> bool:
        """Проверяет, что страница открыта"""
        with allure.step("Проверяем открыта ли страница"):
            try:
                return self.wait.until(EC.url_to_be(page))
            except TimeoutException:
                return False

    def is_clickable(self, element) -> bool:
        """Проверяет кликабельность элемента (перекрытие, доступность, отображение на странице)"""
        with allure.step("Проверяем кликабельность веб элемента"):
            overlapping_element = self.driver.execute_script("""
                const rect = arguments[0].getClientRects()[0];
                if (!rect) return null;  // элемент может быть невидим
                const x = rect.left + rect.width / 2;
                const y = rect.top + rect.height / 2;
                return document.elementFromPoint(x, y);
            """, element)
            if element.is_enabled() and self.is_visible(element) and overlapping_element == element:
                return True
            else:
                return False

    def is_visible(self, element) -> bool:
        """Проверяет видим ли элемент на странице"""
        return element.is_displayed() and self.is_in_viewport(element)

    def move_last_handle(self) -> None:
        """Переход на последнюю открытую вкладку"""
        with allure.step("Переходим на открытую вкладку"):
            tabs = self.driver.window_handles
            self.driver.switch_to.window(tabs[-1])

    def scroll_to(self, element) -> None:
        """Мгновенный скролл до элемента с его отображением в середине страницы"""
        with allure.step("Скроллим до элемента"):
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});", element)

    def scroll_down(self) -> None:
        """Скролл в самый низ страницы"""
        with allure.step("Скроллим вниз страницы"):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_top(self) -> None:
        """Скролл в самый верх страницы"""
        with allure.step("Скроллим вверх страницы"):
            self.driver.execute_script("window.scrollTo(0, 0)")

    def is_in_viewport(self, element) -> bool:
        """Проверка реального отображения элемента в границах экрана"""
        return self.driver.execute_script("""
            const rect = arguments[0].getBoundingClientRect();
            return (
                rect.top >= 0 &&
                rect.left >= 0 &&
                rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.right <= (window.innerWidth || document.documentElement.clientWidth)
            );
        """, element)

    def is_stable(self, element, timeout=0.5):
        rect1 = element.rect
        time.sleep(timeout)
        rect2 = element.rect
        return rect1 == rect2
