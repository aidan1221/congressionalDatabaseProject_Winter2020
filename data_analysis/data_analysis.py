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

# red_blue = ["ff0000", "0000ff"]
#
#
# ratio_bills_passed_per_rep = pd.read_csv('bill_ratio_2.csv')
#
# plt.figure(figsize=(20, 5))
# sb.barplot(x="state", y="ratio", hue="congress", data=ratio_bills_passed_per_rep)
# plt.show()




# Bill statuses
# Introduced
# Became Law
# Passed House
# Became Private Law
# Passed Senate
# Resolving Differences
# Failed House

dem_color_palette_list = ['#009ACD', '#ADD8E6', '#63D1F4', '#0EBFE9', '#C1F0F6']

repub_color_palette_list = ['#FD0202', '#FA2D2D', '#FC5050', '#FC7272', '#FC9C9C']

fig_size = (8,9)
_dpi = 100
start_angle = 180

label_distance = 1.4

text1x = 0.3
text1y = 1
text2x = -1.0
text2y = 2.0

legendxy = (0.8,0.85)

def republican115_house_bills_status():
    r_house_bills_115 = pd.read_csv('R_house_bills_115.csv')

    count_dict = dict()
    count_dict['Introduced'] = [0, 0]
    count_dict['Passed House'] = [0, 0]
    count_dict['Failed House'] = [0, 0]
    count_dict['Passed Senate'] = [0, 0]
    count_dict['Became Law'] = [0, 0]
    count_dict['To President'] = [0, 0]
    count_dict['Became Private Law'] = [0, 0]
    count_dict['Resolving Differences'] = [0, 0]
    count_dict['Total'] = 0

    dict_keys = count_dict.keys()

    for _, row in r_house_bills_115.iterrows():
        if row['status'] in dict_keys:
            count_dict[row['status']][0] += 1
            count_dict['Total'] += 1

    for key in count_dict.keys():
        if key != 'Total':
            count_dict[key][1] = (count_dict[key][0] / count_dict['Total']) * 100

    fig, ax = plt.subplots(figsize=fig_size, dpi=_dpi)

    labels = ["Introduced (" + str(count_dict["Introduced"][0]) + ")",
              "Passed House (" + str(count_dict["Passed House"][0]) + ")",
              "Passed Senate (" + str(count_dict["Passed Senate"][0]) + ")",
              "Became Law (" + str(count_dict["Became Law"][0]) + ")"]

    percentages = [count_dict["Introduced"][1], count_dict["Passed House"][1], count_dict["Passed Senate"][1],
                   count_dict["Became Law"][1]]

    ax.pie(percentages, labels=labels, autopct='%.2f%%',
           shadow=True, startangle=start_angle, colors=repub_color_palette_list,
           pctdistance=1.2, labeldistance=label_distance)

    ax.axis('equal')

    ax.text(text1x, text1y, "*TOTAL BILLS INTRODUCED = 3876")
    ax.text(text2x, text2y, "Republican Sponsored House Bill statuses 115th congress")

    ax.legend(loc=legendxy)
    # ax.set_title("Republican Sponsored House Bill statuses 115th congress")

    plt.show()

    fig.savefig("republican115_house_bills_percent_status.png", format="png")


def democrat115_house_bills_statuses():
    d_house_bills_115 = pd.read_csv('D_house_bills_115.csv')

    count_dict = dict()
    count_dict['Introduced'] = [0, 0]
    count_dict['Passed House'] = [0, 0]
    count_dict['Failed House'] = [0, 0]
    count_dict['Passed Senate'] = [0, 0]
    count_dict['Became Law'] = [0, 0]
    count_dict['To President'] = [0, 0]
    count_dict['Became Private Law'] = [0, 0]
    count_dict['Resolving Differences'] = [0, 0]
    count_dict['Total'] = 0

    dict_keys = count_dict.keys()

    for _, row in d_house_bills_115.iterrows():
        if row['status'] in dict_keys:
            count_dict[row['status']][0] += 1
            count_dict['Total'] += 1

    for key in count_dict.keys():
        if key != 'Total':
            count_dict[key][1] = (count_dict[key][0] / count_dict['Total']) * 100

    fig, ax = plt.subplots(figsize=fig_size, dpi=_dpi)

    labels = ["Introduced (" + str(count_dict["Introduced"][0]) + ")",
              "Passed House (" + str(count_dict["Passed House"][0]) + ")",
              "Passed Senate (" + str(count_dict["Passed Senate"][0]) + ")",
              "Became Law (" + str(count_dict["Became Law"][0]) + ")"]

    percentages = [count_dict["Introduced"][1], count_dict["Passed House"][1], count_dict["Passed Senate"][1],
                   count_dict["Became Law"][1]]

    ax.pie(percentages, labels=labels, autopct='%.2f%%',
           shadow=False, startangle=start_angle, colors=dem_color_palette_list,
           pctdistance=1.2, labeldistance=label_distance)

    ax.axis('equal')

    ax.text(text1x, text1y, "*TOTAL BILLS INTRODUCED = 3467")
    ax.text(text2x, text2y, "Dem Sponsored House Bill statuses 115th congress")

    ax.legend(loc=legendxy)
    # ax.set_title("Dem Sponsored House Bill statuses 115th congress")

    plt.show()

    fig.savefig("democrats115_house_bills_percent_status.png", format="png")


def republican116_house_bills_status():
    r_house_bills_116 = pd.read_csv('R_house_bills_116.csv')

    count_dict = dict()
    count_dict['Introduced'] = [0, 0]
    count_dict['Passed House'] = [0, 0]
    count_dict['Failed House'] = [0, 0]
    count_dict['Passed Senate'] = [0, 0]
    count_dict['Became Law'] = [0, 0]
    count_dict['To President'] = [0, 0]
    count_dict['Became Private Law'] = [0, 0]
    count_dict['Resolving Differences'] = [0, 0]
    count_dict['Total'] = 0

    dict_keys = count_dict.keys()

    for _, row in r_house_bills_116.iterrows():
        if row['status'] in dict_keys:
            count_dict[row['status']][0] += 1
            count_dict['Total'] += 1

    for key in count_dict.keys():
        if key != 'Total':
            count_dict[key][1] = (count_dict[key][0] / count_dict['Total']) * 100

    fig, ax = plt.subplots(figsize=fig_size, dpi=_dpi)

    labels = ["Introduced (" + str(count_dict["Introduced"][0]) + ")",
              "Passed House (" + str(count_dict["Passed House"][0]) + ")",
              "Passed Senate (" + str(count_dict["Passed Senate"][0]) + ")",
              "Became Law (" + str(count_dict["Became Law"][0]) + ")"]

    percentages = [count_dict["Introduced"][1], count_dict["Passed House"][1], count_dict["Passed Senate"][1],
                   count_dict["Became Law"][1]]

    ax.pie(percentages, labels=labels, autopct='%.2f%%',
           shadow=False, startangle=start_angle, colors=repub_color_palette_list,
           pctdistance=1.2, labeldistance=label_distance)

    ax.axis('equal')

    ax.text(text1x, text1y, "*TOTAL BILLS INTRODUCED = 1890")
    ax.text(text2x, text2y, "Republican Sponsored House Bill statuses 116th congress")

    ax.legend(loc=legendxy)
    # ax.set_title("Republican Sponsored House Bill statuses 116th congress")

    plt.show()

    fig.savefig("republican116_house_bills_percent_status.png", format="png")


def democrat116_house_bills_statuses():
    d_house_bills_116 = pd.read_csv('D_house_bills_116.csv')

    count_dict = dict()
    count_dict['Introduced'] = [0, 0]
    count_dict['Passed House'] = [0, 0]
    count_dict['Failed House'] = [0, 0]
    count_dict['Passed Senate'] = [0, 0]
    count_dict['Became Law'] = [0, 0]
    count_dict['To President'] = [0, 0]
    count_dict['Became Private Law'] = [0, 0]
    count_dict['Resolving Differences'] = [0, 0]
    count_dict['Total'] = 0

    dict_keys = count_dict.keys()

    for _, row in d_house_bills_116.iterrows():
        if row['status'] in dict_keys:
            count_dict[row['status']][0] += 1
            count_dict['Total'] += 1

    for key in count_dict.keys():
        if key != 'Total':
            count_dict[key][1] = (count_dict[key][0] / count_dict['Total']) * 100

    fig, ax = plt.subplots(figsize=fig_size, dpi=_dpi)

    labels = ["Introduced (" + str(count_dict["Introduced"][0]) + ")",
              "Passed House (" + str(count_dict["Passed House"][0]) + ")",
              "Passed Senate (" + str(count_dict["Passed Senate"][0]) + ")",
              "Became Law (" + str(count_dict["Became Law"][0]) + ")"]

    percentages = [count_dict["Introduced"][1], count_dict["Passed House"][1], count_dict["Passed Senate"][1],
                   count_dict["Became Law"][1]]

    ax.pie(percentages, labels=labels, autopct='%.2f%%',
           shadow=False, startangle=start_angle, colors=dem_color_palette_list,
           pctdistance=1.2, labeldistance=label_distance)

    ax.axis('equal')

    ax.text(text1x, text1y, "*TOTAL BILLS INTRODUCED = 3885")
    ax.text(text2x, text2y, "Dem Sponsored House Bill statuses 116th congress")

    ax.legend(loc=legendxy)

    # ax.set_title("Dem Sponsored House Bill statuses 116th congress", )

    plt.show()

    fig.savefig("democrats116_house_bills_percent_status.png", format=None)

# pd.set_option('max_rows', None)
#
# print(bills_per_rep_data_116)
#
# bills_per_rep_data_116.plot(kind='bar', x='state', y='bills_per_rep', figsize=(20, 5))
#
# plt.show()
#
republican115_house_bills_status()
democrat115_house_bills_statuses()
republican116_house_bills_status()
democrat116_house_bills_statuses()