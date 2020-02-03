from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd


class Webscraper:

    # class params
    # instantiates webdriver
    DRIVER = webdriver.Chrome("./chromedriver");
    CSS_SELECTOR = By.CSS_SELECTOR

    # Utility methods
    def wait_for_element_invisible_by_css(self, css_selector, duration=10):
        """
        Waits for element invisibility by css selector
        :param css_selector: the css selector selenium for use for the wait condition
        :param duration: the duration of time the driver will wait before throwing an exception
        :return: void
        """

        load_condition = EC.invisibility_of_element((By.CSS_SELECTOR, css_selector))

        WebDriverWait(self.DRIVER, duration).until(load_condition)

    def wait_for_element_visible_by_css(self, css_selector, duration=10):

        load_condition = EC.visibility_of_element((By.CSS_SELECTOR, css_selector))

        WebDriverWait(self.DRIVER, duration).until(load_condition)

    def open(self, url):
        self.DRIVER.get(url)

    # def click_element_by_css(self, css_selector):