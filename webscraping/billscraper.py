from webscraper import Webscraper


class Billscraper(Webscraper):

    URL_116 = "https://www.congress.gov/search?q=%7B%22source%22%3A%22legislation%22%2C%22congress%22%3A%22116" \
              "%22%2C%22chamber%22%3A%22House%22%2C%22type%22%3A%22bills%22%7D"
    URL_115 = "https://www.congress.gov/search?q={%22source%22:%22legislation%22,%22chamber%22:%22House%22,%22" \
              "type%22:%22bills%22,%22congress%22:115}&searchResultViewType=expanded&KWICView=false"

    def __init__(self, chamber, congressionalClass):
        super(Billscraper, self).__init__()
        self.chamber = chamber
        self.congressionalClass = congressionalClass

    def getHouseLegislationPage(self):

        if self.congressionalClass == 116:
            url = self.URL_116

        self.open_url(url)