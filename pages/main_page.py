from base.base_page import BasePage
from config import config


class MainPage(BasePage):
    page_url = config.all_excursion_url
    all_excursion_btn = ("xpath", "//div/ul/li/a[contains(text(), 'Все экскурсии')]")
    report_btn = ("xpath", "//div/p/a[@href='/About/Contact#from-feedback']")

    def excursions(self):
        return self.driver.driver.find_elements("xpath", "//div[@class='col']/div/div")
