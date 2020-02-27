import pandas as pd
import matplotlib.pyplot as plt
import psycopg2 as pg
import seaborn as sb

bills_per_rep_data_116 = pd.read_csv("ratio_bills_passed_per_rep_116.csv")

plt.figure(figsize=(20, 5))
sb.barplot("state", "bills_per_rep", data=bills_per_rep_data_116)\
    .get_figure()\
    .savefig('bills_per_rep.png')
plt.show()



# pd.set_option('max_rows', None)
#
# print(bills_per_rep_data_116)
#
# bills_per_rep_data_116.plot(kind='bar', x='state', y='bills_per_rep', figsize=(20, 5))
#
# plt.show()