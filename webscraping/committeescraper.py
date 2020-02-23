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
    HOUSE_CLERK_URL = "http://clerk.house.gov/"

    # ===========
    # SELECTORS
    # ===========

    HOUSE_COMMITTEE_UL = "table.committeesLandingTable > tbody > tr:nth-child(2) > td:nth-child(1) > ul.plain.margin7 " \
                         "> li > a"
    HOUSE_COMMITTEE_LI = "table.committeesLandingTable > tbody > tr:nth-child(2) > td:nth-child(1) > ul.plain.margin7 " \
                         "> li:nth-child({}) > a"

    HOUSE_SUBCOMMITTEE_UL = "#subcom_list > ul > li > a"
    HOUSE_SUBCOMMITTEE_LI = "#subcom_list > ul > li:nth-child({}) > a"

    MEMBERS_LINK = "#content > div.featured.committee-detail > div.overview_wrapper.bill > div.tertiary > div > ul > " \
        "li:nth-child(2) > a"

    HOUSE_SUBORDINATE_LINK = "#subcom_title > p:nth-child(2) > a"

    HOUSE_MAJORITY_LINKS = "#primary_group > ol > li > a"
    HOUSE_MINORITY_LINKS = "#secondary_group > ol > li > a"
    HOUSE_CLERK_IMG = "#page_content > h2 > img"

    def __init__(self, verbose=True):
        super().__init__(verbose)

    def scrape_committees(self):
        """ Navigates to the congress.gov committee page for instantiated
            Congressional chamber (House or Senate)
         """
        house_subcommittee_dict = dict()
        house_subcommittee_member_dict = dict()
        house_member_dict = dict()
        house_leadership_dict = dict()

        self.open_url(self.COMMITTEES_URL)
        main_window = self.DRIVER.current_window_handle

        committee_items = self.find_elements_by_css(self.HOUSE_COMMITTEE_UL)
        num_committees = len(committee_items)

        for i in range(1, num_committees + 1):
            print("Beginning of for loop")
            item = self.DRIVER.find_element_by_css_selector(self.HOUSE_COMMITTEE_LI.format(i))
            committee_name = item.text
            print(committee_name)

            house_subcommittee_dict[committee_name] = []
            house_member_dict[committee_name] = []
            house_leadership_dict[committee_name] = []


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

            self.wait_for_element_present_by_css(self.HOUSE_CLERK_IMG)

            print("Getting majority members")
            majority_membership_links = self.find_elements_by_css(self.HOUSE_MAJORITY_LINKS)

            for link in majority_membership_links:
                member_name = link.text
                house_member_dict[committee_name].append(member_name)

            print("Getting minority members")
            minority_membership_links = self.find_elements_by_css(self.HOUSE_MINORITY_LINKS)

            for link in minority_membership_links:
                member_name = link.text
                house_member_dict[committee_name].append(member_name)

            print("Getting committee leadership (chair, ranking member)")
            leadership = (majority_membership_links[0].text, minority_membership_links[0].text)
            house_leadership_dict[committee_name].append(leadership)

            # Get subcommittees
            house_member_dict, house_subcommittee_member_dict, house_subcommittee_dict = self.scrape_house_subcommittee(committee_name, house_subcommittee_dict, house_subcommittee_member_dict, house_member_dict)

        print("Data collected successfully")
        self.DRIVER.quit()

        return house_member_dict, house_subcommittee_member_dict, house_subcommittee_dict, house_leadership_dict

    def scrape_house_subcommittee(self, committee_name, subcommittee_dict, subcommittee_member_dict, member_dict):
        current_url = self.DRIVER.current_url
        assert self.HOUSE_CLERK_URL in str(current_url), "ummmm what?"

        self.wait_for_element_present_by_css(self.HOUSE_CLERK_IMG)

        print("Getting subcommittees")
        subcommittees_items = self.find_elements_by_css(self.HOUSE_SUBCOMMITTEE_UL)
        num_subcommittees = len(subcommittees_items)

        for i in range(1, num_subcommittees + 1):
            item = self.DRIVER.find_element_by_css_selector(self.HOUSE_SUBCOMMITTEE_LI.format(i))
            subcommittee_name = item.text
            print(subcommittee_name)
            subcommittee_name = committee_name + " - " + subcommittee_name
            subcommittee_dict[committee_name].append(subcommittee_name)
            subcommittee_member_dict[subcommittee_name] = []

            item.click()
            time.sleep(2)

            print("Getting subcommittee majority members")
            subcommittee_majority_membership_links = self.find_elements_by_css(self.HOUSE_MAJORITY_LINKS)
            for majority_link in subcommittee_majority_membership_links:
                member_name = majority_link.text
                subcommittee_member_dict[subcommittee_name].append(member_name)

            print("Getting subcommittee minority members")
            subcommittee_minority_membership_links = self.find_elements_by_css(self.HOUSE_MINORITY_LINKS)

            for minority_link in subcommittee_minority_membership_links:
                member_name = minority_link.text
                subcommittee_member_dict[subcommittee_name].append(member_name)

            print(subcommittee_dict)
            print(subcommittee_member_dict)

            print("On subcommittee detail page")
            subordinate_of_link = self.find_element_by_css(self.HOUSE_SUBORDINATE_LINK)

            print("Clicking subordinate of link")
            subordinate_of_link.click()
            time.sleep(3)

        self.DRIVER.close()
        time.sleep(5)
        self.DRIVER.switch_to.window(self.DRIVER.window_handles[0])

        print("Returning to committees page")
        self.DRIVER.get("https://www.congress.gov/committees")

        return member_dict, subcommittee_member_dict, subcommittee_dict

        # ADD senate_subcommittee_scraper

        # 115th congress: https://github.com/unitedstates/congress-legislators/blob/fc5647af4535a397710afa98dd97eef2516253ac/committee-membership-current.yaml
        # 116th congress: https://github.com/unitedstates/congress-legislators/blob/master/committee-membership-current.yaml


