from webscraper import Webscraper


class Billscraper(Webscraper):

    HOUSE_116 = "https://www.congress.gov/search?q=%7B%22source%22%3A%22legislation%22%2C%22congress%22%3A%22116" \
              "%22%2C%22chamber%22%3A%22House%22%2C%22type%22%3A%22bills%22%7D"
    HOUSE_115 = "https://www.congress.gov/search?q={%22source%22:%22legislation%22,%22chamber%22:%22House%22,%22" \
              "type%22:%22bills%22,%22congress%22:115}&searchResultViewType=expanded&KWICView=false"

    def __init__(self, chamber, congressionalClass, verbose=True):
        super().__init__(verbose)
        self.chamber = chamber
        self.congressionalClass = congressionalClass

    def get_house_legislation_page(self):

        """ Navigates to the appropriate search results page for constructed House class (115 or 116)"""

        self.log(f"Getting House legislation page for {self.congressionalClass}th Congress")

        if self.congressionalClass == 116:
            url = self.HOUSE_116
        else:
            url = self.HOUSE_115

        self.open_url(url)

    def get_number_of_search_pages(self):

        """ Gets the number of total pages for the given search (class, chamber, legislation type).

            Returns total number of pages as int
        """

        self.log("Getting total number of pages for search")

        page_selector = "#searchTune > div.basic-search-tune-number > div > span.results-number"
        page_element = self.find_element_by_css(page_selector)

        return int(page_element.text).split()[1]

    def wait_for_page_loaded(self, duration=10):

        page_load_selector = "body > div.actionLoaderWrapper"
