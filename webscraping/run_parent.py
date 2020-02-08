from webscraper import Webscraper
from billscraper import Billscraper

bs = Billscraper("house", 115)
bs.scrape_bills()