import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
import psycopg2 as pg
import seaborn as sb

# bills_per_rep_data_116 = pd.read_csv("ratio_bills_passed_per_rep_116.csv")
#
# plt.figure(figsize=(20, 5))
# sb.barplot("state", "bills_per_rep", data=bills_per_rep_data_116, color='blue')\
#     .get_figure()\
#     .savefig('ratio_bills_passed_per_rep_116.png')
# plt.show()
#
# bills_per_rep_data_115 = pd.read_csv("ratio_bills_passed_per_rep_115.csv")
#
# plt.figure(figsize=(20, 5))
# sb.barplot("state", "ratio_bills_passed_per_rep", data=bills_per_rep_data_115, color='red')\
#     .get_figure()\
#     .savefig('ratio_bills_passed_per_rep_115.png')
# plt.show()

red_blue = ["ff0000", "0000ff"]


ratio_bills_passed_per_rep = pd.read_csv('bill_ratio_2.csv')

plt.figure(figsize=(20, 5))
sb.barplot(x="state", y="ratio", hue="congress", data=ratio_bills_passed_per_rep)
plt.show()


# pd.set_option('max_rows', None)
#
# print(bills_per_rep_data_116)
#
# bills_per_rep_data_116.plot(kind='bar', x='state', y='bills_per_rep', figsize=(20, 5))
#
# plt.show()