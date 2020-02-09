from webscraper import Webscraper
import sys


class Billscraper(Webscraper):

    # ===========
    # URLs
    # ===========

    HOUSE_116 = "https://www.congress.gov/search?q=%7B%22source%22%3A%22legislation%22%2C%22congress%22%3A%22116" \
        "%22%2C%22chamber%22%3A%22House%22%2C%22type%22%3A%22bills%22%7D"
    HOUSE_115 = "https://www.congress.gov/search?q={%22source%22:%22legislation%22,%22chamber%22:%22House%22,%22" \
        "type%22:%22bills%22,%22congress%22:115}&searchResultViewType=expanded&KWICView=false"

    SENATE_116 = ""

    SENATE_115 = ""

    # ===========
    # SELECTORS
    # ===========

    NEXT_PAGE_SELECTOR = "#searchTune > div.basic-search-tune-number > div > a.next > i"

    def __init__(self, chamber, congressional_class, verbose=True):
        super().__init__(verbose)
        self.chamber = chamber
        self.congressional_class = congressional_class
        self.bill_count = 0


    def scrape_bills(self):

        """ Scrapes the bills data on congress.gov for instantiated Chamber and Congressional class """

        self.get_legislation_page()

        self.wait_for_page_loaded()

        number_of_pages = self.get_number_of_search_pages()

        data_dict = self.build_data_dict(["names", "descriptions", "statuses", "bill_committees", "sponsors"])

        for i in range(number_of_pages):
            self.wait_for_page_loaded()
            self.get_page_data(data_dict)

            assert len(data_dict["names"]) == self.bill_count, "len(names) = {} -- should be {}"\
                .format(len(data_dict["names"]), self.bill_count)
            assert len(data_dict["descriptions"]) == self.bill_count, "len(descriptions) = {} -- should be {}" \
                .format(len(data_dict["descriptions"]), self.bill_count)
            assert len(data_dict["statuses"]) == self.bill_count, "len(statuses) = {} -- should be {}" \
                .format(len(data_dict["statuses"]), self.bill_count)
            assert len(data_dict["bill_committees"]) == self.bill_count, "len(bill_committees) = {} -- should be {}" \
                .format(len(data_dict["bill_committees"]), self.bill_count)
            assert len(data_dict["sponsors"]) == self.bill_count, "len(sponsors) = {} -- should be {}" \
                .format(len(data_dict["sponsors"]), self.bill_count)

            current_page = i + 1
            self.click_to_next_page(current_page, number_of_pages)

        print(data_dict)




    def get_legislation_page(self):

        """ Navigates to the appropriate search results page for instantiated
            Congressional chamber (House or Senate) and class (115 or 116)
        """

        if self.chamber.lower() == "house":

            if self.congressional_class == 116:
                url = self.HOUSE_116
            else:
                url = self.HOUSE_115

            self.log(f"Getting HOUSE legislation page for {self.congressional_class}th Congress")

        elif self.chamber.lower() == "senate":

            if self.congressional_class == 116:
                url = self.SENATE_116
            else:
                url = self.SENATE_115

            self.log(f"Getting SENATE legislation page for {self.congressional_class}th Congress")

        else:
            self.log(f"ERROR - '{self.chamber}' is not a valid option for legislation scraping")
            sys.exit(1)

        self.open_url(url)

    def get_page_data(self, data_dict):

        """ Parses beautiful soup object of current page's html for desired bill data """

        soup = self.get_html_soup()

        bills = soup.findAll('li', attrs={'class': 'expanded'})

        for bill in bills:
            try:
                for item in bill.findAll('span', attrs={'class':'result-heading'}):
                    data_dict["names"].append(item.find('a').text)
                data_dict["descriptions"].append(bill.find('span', attrs={'class': 'result-title'}).text)
                for item in bill.findAll('span', attrs={'class': 'result-item result-tracker'}):
                    data_dict["statuses"].append((' ').join(item.findAll('p', attrs={'class': 'hide_fromsighted'})[0].text.split()[5:]))
                data_dict["bill_committees"].append(bill.findAll('span', attrs={'class': 'result-item'})[1].text.split('-')[1])
                data_dict["sponsors"].append(bill.findAll('span', attrs={'class': 'result-item'})[0].find('a').text)
                self.bill_count += 1
            except Exception as err:
                print(err)
                continue

    def click_to_next_page(self, current_page, num_pages):

        """ Clicks the next page button if not on the last page

            current_page -- the current page # of the search
            num_pages -- the total number of pages in the search
        """

        if current_page != num_pages:

            self.log(f"Clicking to the next page - {current_page + 1}")

            # assert len(names) == 100 * (current_page+1), "len(names) = {}".format(len(names))
            next_page_button = self.find_element_by_css(self.NEXT_PAGE_SELECTOR)
            next_page_button.click()

        else:
            self.log(f"Last page reached - {current_page}")

    def get_number_of_search_pages(self):

        """ Gets the number of total pages for the given search (class, chamber, legislation type).

            Returns total number of pages as int
        """

        self.log("Getting total number of pages for search")

        page_selector = "#searchTune > div.basic-search-tune-number > div > span.results-number"
        page_element = self.find_element_by_css(page_selector)

        return int(page_element.text.split()[1])

    def wait_for_page_loaded(self, duration=10):

        """ Waits for the Congress.gov loading spinner to be hidden

            duration -- amount of time driver will wait for condition
        """

        self.log("Waiting for page loaded")

        page_load_selector = "body > div.actionLoaderWrapper"
        self.wait_for_element_to_have_attribute(page_load_selector, "style", "none", duration)

        self.log("Page loaded")
