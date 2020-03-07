from webscraper import Webscraper
from billscraper import Billscraper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


HOUSE = "house"
SENATE = "senate"
CONGRESS = [115, 116]

bs = Billscraper(True)

# for num in CONGRESS:
#     bs.scrape_bills(HOUSE, num)
#     bs.scrape_bills(SENATE, num)
#
# bs.quit_driver()


# bs.scrape_co_sponsors("house", 116)

finish = False
while not finish:
    try:
        finish = bs.get_cosponsors_new()
    except Exception as e:
        bs.quit_driver()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--window-size=1920x1080')
        bs.DRIVER = webdriver.Chrome(chrome_options=chrome_options, executable_path='./chromedriver78')
        print("ERROR: ", e)
        finish = False
