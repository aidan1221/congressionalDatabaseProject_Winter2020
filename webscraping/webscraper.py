from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd


class Webscraper:

    # Webdriver initialization
    DRIVER = webdriver.Chrome("./chromedriver")

    # Common params
    CSS_SELECTOR = By.CSS_SELECTOR

    def __int__(self, verbose=True):
        self.VERBOSE = verbose

    # ========================
    # Selenium Utility methods
    # ========================

    def wait_for_element_invisible_by_css(self, css_selector, duration=10):

        """ Waits for element invisibility by CSS selector """

        load_condition = EC.invisibility_of_element((By.CSS_SELECTOR, css_selector))

        WebDriverWait(self.DRIVER, duration).until(load_condition)

    def wait_for_element_visible_by_css(self, css_selector, duration=10):

        """ Waits for element visibility by CSS selector """

        load_condition = EC.visibility_of_element((By.CSS_SELECTOR, css_selector))

        WebDriverWait(self.DRIVER, duration).until(load_condition)

    def open_url(self, url):
        self.DRIVER.get(url)

    def click_element_by_css(self, css_selector):

        """ Clicks element found by CSS selector """

        element = self.DRIVER.find_elements_by_css_selector(css_selector)

        element.click()

    def wait(self, duration=10):
        time.sleep(duration)

    # ========================
    # Beautiful Soup Methods
    # ========================

    def get_html(self):

        """ Returns a BeautifulSoup object of current page's HTML """

        content = self.DRIVER.page_source
        return BeautifulSoup(content, 'html.parser')

    # ========================
    # Console Logger
    # ========================

    def log(self, message):

        """
        prints log messages to the console
        self.VERBOSE set in constructor -> default behavior True
        """

        if self.VERBOSE:
            print(message)