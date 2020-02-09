from webscraper import Webscraper
from billscraper import Billscraper


bs = Billscraper("house", 116, True)

bs.scrape_bills()

bs.quit_driver()