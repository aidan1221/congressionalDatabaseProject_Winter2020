
from csv_editing import CSV_Editor as csve
import pandas as pd

house_reps_116 = "../csv_data/house_reps_116.csv"
house_reps_115 = "../csv_data/house_reps_115.csv"
senators_116 = "../csv_data/senators_116.csv"
senators_115 = "../csv_data/senators_115.csv"

house_bills_116 = "../csv_data/house_bills_116.csv"
house_bills_115 = "../csv_data/house_bills_115.csv"
senate_bills_116 = "../csv_data/senate_bills_116.csv"
senate_bills_115 = "../csv_data/senate_bills_115.csv"


# csve.clean_house_representative_data_csv(house_reps_116)
# csve.clean_house_representative_data_csv(house_reps_115)
#
# csve.clean_house_representative_data_csv(senators_116)
# csve.clean_house_representative_data_csv(senators_115)


# csve.clean_bills_names(house_bills_116, "house", 116)
# csve.clean_bills_names(house_bills_115, "house", 115)
csve.clean_bills_names(senate_bills_115, "senate", 115)
csve.clean_bills_names(senate_bills_116, "senate", 116)