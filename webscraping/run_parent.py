from webscraper import Webscraper
from billscraper import Billscraper

ws = Webscraper()

ws.open_url("https://www.google.com")

ws.close()

bs = Billscraper(115, "house")
