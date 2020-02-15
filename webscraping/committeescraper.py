import time

from webscraper import Webscraper

class Committeescraper(Webscraper):
    # Class params for css selectors
    # Convert UTF-8 to ascii due to special characters
    # Assert length of data lists - make sure all columns have same length, make descriptive

    # ===========
    # URLs
    # ===========

    COMMITTEES_URL = "https://www.congress.gov/committees"

    # ===========
    # SELECTORS
    # ===========

    HOUSE_COMMITTEE_UL = "table.committeesLandingTable > tbody > tr:nth-child(2) > td:nth-child(1) > ul.plain.margin7 " \
                         "> li > a "

    HOUSE_COMMITTEE_LI = "table.committeesLandingTable > tbody > tr:nth-child(2) > td:nth-child(1) > ul.plain.margin7 " \
                         "> li:nth-child({}) > a"

    MEMBERS_LINK = "#content > div.featured.committee-detail > div.overview_wrapper.bill > div.tertiary > div > ul > " \
        "li:nth-child(2) > a"

    SUBCOMMITTEE_LINKS = "#subcom_list > ul > li > a"
    MAJORITY_LINKS = "#primary_group > ol > li > a"
    MINORITY_LINKS = "#secondary_group > ol > li > a"
    CLERK_IMG = "#page_content > h2 > img"

    def __init__(self, verbose=True):
        super().__init__(verbose)


    def scrape_committees(self):
        """ Navigates to the congress.gov committee page for instantiated
            Congressional chamber (House or Senate)
         """
        committee_subcommittee_dict = dict()
        committee_member_dict = dict()

        self.open_url(self.COMMITTEES_URL)
        main_window = self.DRIVER.current_window_handle

        committee_items = self.find_elements_by_css(self.HOUSE_COMMITTEE_UL)
        num_committees = len(committee_items)

        for i in range(1, num_committees + 1):
            print("Beginning of for loop")
            item = self.DRIVER.find_element_by_css_selector(self.HOUSE_COMMITTEE_LI.format(i))
            committee_name = item.text
            print(committee_name)

            committee_subcommittee_dict[committee_name] = []
            committee_member_dict[committee_name] = []

            item.click()

            time.sleep(2)

            print("On committee detail page")
            committee_membership_link = self.find_element_by_css(self.MEMBERS_LINK)

            print("Clicking committee membership link")
            committee_membership_link.click()

            time.sleep(3)

            handles = self.DRIVER.window_handles
            for handle in handles:
                if handle != main_window:
                    self.DRIVER.switch_to.window(handle)

            current_url = self.DRIVER.current_url
            print(current_url)
            assert "http://clerk.house.gov/" in str(current_url), "ummmm what?"

            self.wait_for_element_present_by_css(self.CLERK_IMG)

            print("Getting subcomittees")
            subcommittees_links = self.find_elements_by_css(self.SUBCOMMITTEE_LINKS)

            for link in subcommittees_links:
                subcommittee_name = link.text
                committee_subcommittee_dict[committee_name].append(subcommittee_name)

            print("Getting majority members")
            majority_membership_links = self.find_elements_by_css(self.MAJORITY_LINKS)

            for link in majority_membership_links:
                member_name = link.text
                committee_member_dict[committee_name].append(member_name)

            print("Getting minority members")
            minority_membership_links = self.find_elements_by_css(self.MINORITY_LINKS)

            for link in minority_membership_links:
                member_name = link.text
                committee_member_dict[committee_name].append(member_name)

            print(committee_subcommittee_dict)
            print(committee_member_dict)

            self.DRIVER.close()

            time.sleep(5)

            self.DRIVER.switch_to.window(self.DRIVER.window_handles[0])

            print("Returning to committees page")
            self.DRIVER.get("https://www.congress.gov/committees")

        print("Data collected successfully")
        return committee_member_dict, committee_subcommittee_dict

        self.DRIVER.quit()
