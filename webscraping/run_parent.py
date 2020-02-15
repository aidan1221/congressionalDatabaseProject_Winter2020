from datetime import time

from webscraper import Webscraper
from billscraper import Billscraper
from committeescraper import Committeescraper


# bs = Billscraper("house", 116, True)
# bs.scrape_bills()
# bs.close()


cs = Committeescraper()
cs.scrape_committees()
cs.close()



time.sleep(10)
