from webscraper import Webscraper
from billscraper import Billscraper
from rollcallscraper import Rollcallscraper

RS = Rollcallscraper()
RS.roll_call_scrape(115)
RS.roll_call_scrape(116)
RS.quit_driver()

HOUSE = "house"
SENATE = "senate"
CONGRESS = [115, 116]

bs = Billscraper(False)

# for num in CONGRESS:
#     bs.scrape_bills(HOUSE, num)
#     bs.scrape_bills(SENATE, num)
#
# bs.quit_driver()

# bs.scrape_co_sponsors("house", 116)

# bs.get_cosponsors_new()