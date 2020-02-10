from webscraper import Webscraper
import sys
## assert when count is not same as last class when gathering data, ensure descriptive
##convert UTF8 to ASCII

class Rollcallscraper(Webscraper):
    HOUSE_116_1 = "http://clerk.house.gov/evs/2019/index.asp"
    HOUSE_116_2 = "http://clerk.house.gov/evs/2020/index.asp"
    HOUSE_115_1 = "http://clerk.house.gov/evs/2017/index.asp"
    HOUSE_115_2 = "http://clerk.house.gov/evs/2018/index.asp"

    SENATE_116_1 = "https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_116_1.htm"
    SENATE_116_2 = "https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_116_2.htm"
    SENATE_115_1 = "https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_115_1.htm"
    SENATE_115_2 = "https://www.senate.gov/legislative/LIS/roll_call_lists/vote_menu_115_2.htm"