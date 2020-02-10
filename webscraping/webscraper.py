from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import pandas as pd


class Webscraper(object):

    DRIVER = webdriver.Chrome("./chromedriver.exe")
    VERBOSE = True

    # Common params
    CSS_SELECTOR = By.CSS_SELECTOR

    def __init__(self, headless=False, verbose=True):
        # if headless == True -> run chromedriver headless
        if headless:
            chrome_options = Options()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--window-size=1920x1080')
            self.DRIVER = webdriver.Chrome(chrome_options=chrome_options, executable_path='./chromedriver78')

        self.VERBOSE = verbose

    # ========================
    # Selenium Utility methods
    # ========================

    def open_url(self, url):

        """ Opens the given url with the webdriver.

            url -- URL to be opened with the webdriver
        """
        self.log(f"Opening URL - {url}")
        self.DRIVER.get(url)

    def close(self):

        """ Closes the current window """

        self.log("Closing Webscraper...")
        self.DRIVER.close()

    def find_element_by_css(self, css_selector):

        """ Finds element by given CSS selector

            css_selector -- CSS selector used to find element
        """

        self.log(f"Finding element by CSS - {css_selector}")

        return self.DRIVER.find_element_by_css_selector(css_selector)

    # ========================
    # Selenium Wait methods
    # ========================

    def wait(self, duration=10):

        """ Waits for a period of time

            duration -- wait time (default 10)
        """
        self.log(f"Waiting for {duration} seconds...")
        time.sleep(duration)

    def wait_for_element_invisible_by_css(self, css_selector, duration=10):

        """ Waits for element invisibility by CSS selector.

            css_selector -- CSS selector used to find desired element
            duration -- duration webdriver will wait for invisibility of element before raising exception (default 10)
        """

        self.log(f"Waiting for invisibility of element {css_selector}")

        load_condition = EC.invisibility_of_element((By.CSS_SELECTOR, css_selector))

        WebDriverWait(self.DRIVER, duration).until(load_condition)

    def wait_for_element_visible_by_css(self, css_selector, duration=10):

        """ Waits for element visibility by CSS selector.

            css_selector -- CSS selector used to find desired element
            duration -- duration webdriver will wait to find element before raising exception (default 10)
        """

        self.log(f"Waiting for visibility of element {css_selector}")

        load_condition = EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector))

        WebDriverWait(self.DRIVER, duration).until(load_condition, "Element not found")

    def wait_for_element_present_by_css(self, css_selector, duration=10):

        """ Waits for element to be present by CSS selector.

            css_selector -- CSS selector used to find desired element
            duration -- duration webdriver will wait to find element before raising exception (default 10)
        """

        self.log(f"Waiting for presence of element {css_selector}")

        load_condition = EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))

        WebDriverWait(self.DRIVER, duration).until(load_condition, "Element not found")

    def wait_for_element_to_have_attribute(self, css_selector, attribute, value, duration=10):

        """ Waits for given CSS selector to have specified attribute value

            css_selector -- CSS selector used to find desired element
            attribute -- html attribute to be checked for given value
            value - attribute value waited on
            duration -- wait duration (default 10)
        """

        self.log(f"Waiting for selector - {css_selector} - to have attribute of {attribute}='{value}'")

        selector_with_attribute = f"{css_selector}[{attribute}*='{value}']"
        self.wait_for_element_present_by_css(selector_with_attribute, duration)

    # ========================
    # Selenium Navigation methods
    # ========================

    def click_element_by_css(self, css_selector):

        """ Clicks element found by CSS selector.

            css_selector -- CSS selector used to find desired element
        """

        element = self.DRIVER.find_elements_by_css_selector(css_selector)

        element.click()

    # ========================
    # Beautiful Soup Methods
    # ========================

    def get_html_soup(self):

        """ Returns a BeautifulSoup object of current page's HTML """

        self.log("Retrieving beautiful soup object of HTML")
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
            print(f"*** Log - {message}")

    # ========================
    # General Utility Methods
    # ========================

    def build_data_dict(self, dict_keys):

        """ builds a python dictionary with given keys

            dict_keys -- list of keys to build dictionary with
        """
        data_dict = dict()

        for key in dict_keys:
            data_dict[key] = []

        return data_dict