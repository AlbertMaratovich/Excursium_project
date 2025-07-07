from base.base_page import BasePage
from config import config


class LoginPage(BasePage):
    field_email = ("xpath", "//form/div/input[@type='email']")
    password_field = ("xpath", "//div/form/div[2]/input[@class='form-control fakepassword']")
    login_header = ("xpath", "//li/a[@data-bs-original-title='Войти']")
    login_btn = ("id", "login-btn")
    page_url = config.login_url
