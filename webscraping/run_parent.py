from datetime import time

from webscraper import Webscraper
from billscraper import Billscraper


bs = Billscraper("house", 116, True)

bs.scrape_bills()


bs.close()


# ws.open("https://www.congress.gov")
#
# element = ws.DRIVER.find_element_by_css_selector("#search")
#
# element.send_keys("alabama")
# element.submit()


time.sleep(10)
