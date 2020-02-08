from webscraper import Webscraper
from billscraper import Billscraper


bs = Billscraper("house", 116)

bs.scrape_bills()


bs.close()
