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

    SENATE_116 = "https://www.congress.gov/search?q=%7B%22source%22%3A%22legislation%22%2C%22congress%22%3A%22116" \
                 "%22%2C%22chamber%22%3A%22Senate%22%2C%22type%22%3A%22bills%22%7D"

    SENATE_115 = "https://www.congress.gov/search?q=%7B%22source%22%3A%22legislation%22%2C%22chamber%22%3A%22Senate" \
                 "%22%2C%22type%22%3A%22bills%22%2C%22congress%22%3A115%7D"

    # ===========
    # SELECTORS
    # ===========

    NEXT_PAGE_SELECTOR = "#searchTune > div.basic-search-tune-number > div > a.next > i"

    def __init__(self, headless=False, verbose=True):
        super().__init__(headless, verbose)
        self.BILL_COUNT = 0

    def scrape_bills(self, chamber, congressional_class):

        """ Scrapes the bills data on congress.gov for chamber and congressional class

            chamber -- the chamber of Congress to scrape bills for (string)
            congressional_class -- class 115 or 116 of Congress (int)
        """

        self.log(f"Scraping bills for {chamber} of {congressional_class}th Congress")

        # resets BILL_COUNT to 0 for consecutive scraping sessions
        self.BILL_COUNT = 0

        # builds file name from args for csv file generated from data
        file_name = chamber + '_' + str(congressional_class) + '_' + "bills.csv"

        self.get_legislation_page(chamber, congressional_class)

        self.wait_for_page_loaded()

        number_of_pages = self.get_number_of_search_pages()

        data_dict = self.build_data_dict(["names", "descriptions", "statuses", "bill_committees", "sponsors"])

        for i in range(number_of_pages):
            self.wait_for_page_loaded()
            self.get_page_data(data_dict)

            # each list must be of same length to convert to pandas DataFrame
            assert len(data_dict["names"]) == self.BILL_COUNT, "len(names) = {} -- should be {}"\
                .format(len(data_dict["names"]), self.BILL_COUNT)
            assert len(data_dict["descriptions"]) == self.BILL_COUNT, "len(descriptions) = {} -- should be {}" \
                .format(len(data_dict["descriptions"]), self.BILL_COUNT)
            assert len(data_dict["statuses"]) == self.BILL_COUNT, "len(statuses) = {} -- should be {}" \
                .format(len(data_dict["statuses"]), self.BILL_COUNT)
            assert len(data_dict["bill_committees"]) == self.BILL_COUNT, "len(bill_committees) = {} -- should be {}" \
                .format(len(data_dict["bill_committees"]), self.BILL_COUNT)
            assert len(data_dict["sponsors"]) == self.BILL_COUNT, "len(sponsors) = {} -- should be {}" \
                .format(len(data_dict["sponsors"]), self.BILL_COUNT)

            current_page = i + 1
            self.click_to_next_page(current_page, number_of_pages)

        self.log("Scraping completed... Writing to csv")
        self.csv_from_dict(file_name, data_dict)

    def get_legislation_page(self, chamber, congressional_class):

        """ Navigates to the appropriate search results page for instantiated
            Congressional chamber (House or Senate) and class (115 or 116)
        """

        if chamber.lower() == "house":

            if congressional_class == 116:
                url = self.HOUSE_116
            else:
                url = self.HOUSE_115

            self.log(f"Getting HOUSE legislation page for {congressional_class}th Congress")

        elif chamber.lower() == "senate":

            if congressional_class == 116:
                url = self.SENATE_116
            else:
                url = self.SENATE_115

            self.log(f"Getting SENATE legislation page for {congressional_class}th Congress")

        else:
            self.log(f"ERROR - '{chamber}' is not a valid option for legislation scraping")
            sys.exit(1)

        self.open_url(url)

    def get_page_data(self, data_dict):

        """ Parses beautiful soup object of current page's html for desired bill data """

        self.log("Parsing page for bill data")

        soup = self.get_html_soup()

        bills = soup.findAll('li', attrs={'class': 'expanded'})

        for bill in bills:
            try:

                for item in bill.findAll('span', attrs={'class':'result-heading'}):
                    name = item.find('a').text

                description = bill.find('span', attrs={'class': 'result-title'}).text

                for item in bill.findAll('span', attrs={'class': 'result-item result-tracker'}):
                    status = (' ').join(item.findAll('p', attrs={'class': 'hide_fromsighted'})[0].text.split()[5:])

                bill_committee = bill.findAll('span', attrs={'class': 'result-item'})[1].text.split('-')[1]

                sponsor = bill.findAll('span', attrs={'class': 'result-item'})[0].find('a').text

                self.BILL_COUNT += 1

            except Exception as err:
                self.log_error(err)
                continue

            self.log(f"Bill {name} collected --> adding data to dictionary")
            data_dict["names"].append(name.strip())
            data_dict["descriptions"].append(description.strip())
            data_dict["statuses"].append(status.strip())
            data_dict["bill_committees"].append(bill_committee.strip())
            data_dict["sponsors"].append(sponsor.strip())

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
