
from csv_editing import CSV_Editor as csve
import pandas as pd

house_reps_116 = "../csv_data/house_reps_116.csv"
house_reps_115 = "../csv_data/house_reps_115.csv"
senators_116 = "../csv_data/senators_116.csv"
senators_115 = "../csv_data/senators_115.csv"



# csve.clean_house_representative_data_csv(house_reps_116)
# csve.clean_house_representative_data_csv(house_reps_115)



csve.clean_house_representative_data_csv(senators_116)
csve.clean_house_representative_data_csv(senators_115)