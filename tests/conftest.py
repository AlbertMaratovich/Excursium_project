import pytest
import allure
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--headless") # need to use after debugging
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-dev-shm-usage")# this
    options.add_argument("--disable-gpu") # this
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        " (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    )
    browser = webdriver.Chrome(options=options)
    browser.implicitly_wait(10)
    yield browser
    browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Получаем результат выполнения теста
    outcome = yield
    result = outcome.get_result()

    # Проверяем, упал ли тест
    if result.when == "call" and result.failed:
        driver = item.funcargs.get("driver")  # фикстура должна называться driver
        if driver:
            screenshot = driver.get_screenshot_as_png()
            allure.attach(
                body=screenshot,
                name="Скриншот при падении",
                attachment_type=allure.attachment_type.PNG
            )
