from webscraper import Webscraper
import sys
import csv
## assert when count is not same as last class when gathering data, ensure descriptive
##convert UTF8 to ASCII

class Rollcallscraper(Webscraper):

    """ set URLS
    """
    HOUSE_116_1 = "http://clerk.house.gov/evs/2019/index.asp"
    HOUSE_116_2 = "http://clerk.house.gov/evs/2020/index.asp"
    HOUSE_115_1 = "http://clerk.house.gov/evs/2017/index.asp"
    HOUSE_115_2 = "http://clerk.house.gov/evs/2018/index.asp"

    HOUSE_URLS_115 = [HOUSE_115_1,HOUSE_115_2]
    HOUSE_URLS_116 = [HOUSE_116_1,HOUSE_116_2]
    HOUSE_URLS_LIST = [HOUSE_URLS_115,HOUSE_URLS_116]

    SENATE_116_1 = "https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_116_1.htm"
    SENATE_116_2 = "https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_116_2.htm"
    SENATE_115_1 = "https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_115_1.htm"
    SENATE_115_2 = "https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_115_2.htm"

    """ Initialize RollCallScraper"""
    def __init__(self, headless=False, verbose=True):
        super().__init__(headless,verbose)
        self.bill_count =0
        self.roll_call_dict = self.build_data_dict(['session','roll#','date','issue','question','result','title'])

    def roll_call_scrape(self):
        #call for each house URL

        for SESSION in self.HOUSE_URLS_LIST:
            session_number=115
            for HOUSE_URL in SESSION:
                self.open_url(HOUSE_URL)
                self.get_page_data(HOUSE_URL,session_number)
                self.create_csv_summary(session_number)
                session_number+=1
                self.roll_call_dict = self.build_data_dict(['session','roll#','date','issue','question','result','title'])
        """
        for HOUSE_URL in self.HOUSE_URLS_115:
            self.log("opening page:i")
            self.log(i)
            i+=1
            self.open_url(HOUSE_URL)
            self.get_page_data(HOUSE_URL)
        #self.log(self.roll_call_dict)
        self.log("creating csv")
        self.create_csv_summary('115')

        #clear the dictionary for the next session's data
        self.roll_call_dict = self.build_data_dict(['roll#','date','issue','question','result','title'])
        #self.roll_call_dict = dict((k,None)for k in self.roll_call_dict)
        self.log(self.roll_call_dict)
        for HOUSE_URL in self.HOUSE_URLS_116:
            self.open_url(HOUSE_URL)
            self.get_page_data(HOUSE_URL)
        #self.log(self.roll_call_dict)
        self.log("creating csv")
        self.create_csv_summary('116')
        """

        #call for each senate URL

    def create_csv_summary(self,congress):
        csv_file = str(congress)+"roll_call_summary"
        try:
            with open(csv_file, 'w') as csvfile:
                for key in self.roll_call_dict.keys():
                    csvfile.write("%s,%s\n"%(key,self.roll_call_dict[key]))
        except IOError:
            print("I/O error with CSV creation")

    def get_page_data(self, HOUSE_URL,session_number):
        """parses beautiful soup object of current page's html for desired roll call page"""
        roll_call_links=self.find_elements_by_css('body>font>a')
        self.log(roll_call_links)
        startingpage = HOUSE_URL
        for i in range(0, len(roll_call_links)):
            link = self.find_element_by_css(f"body>font>a:nth-of-type({i+1})")
            self.log("clicking on link")
            link.click()
            self.wait(5)
            self.scrape_roll_call_nav(session_number)
            self.open_url(startingpage)
        #self.DRIVER.close()

    def scrape_roll_call_nav(self,session_number):
        soup = self.get_html_soup()
        table = soup.find('table')
        table_rows = table.find_all('tr')
        for tr in table_rows:
            td = tr.find_all('td')
            row = [i.text for i in td]
            # self.log(row)
            if row:
                self.roll_call_dict["session"].append(session_number)
                self.roll_call_dict["roll#"].append(row[0])
                self.roll_call_dict["date"].append(row[1])
                self.roll_call_dict["issue"].append(row[2])
                self.roll_call_dict["question"].append(row[3])
                self.roll_call_dict["result"].append(row[4])
                self.roll_call_dict["title"].append(row[5])
        #self.log(self.roll_call_dict)




    def get_roll_call_data(self,rollCallPages):
        """gets roll call data from roll call summary page, after you click into the page"""
        self.open_url(rollCallPages)
        self.wait_for_page_loaded()
        #self.roll_call_dict(["roll#"])

