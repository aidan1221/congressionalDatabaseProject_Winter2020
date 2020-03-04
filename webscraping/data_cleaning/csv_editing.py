import pandas as pd


class CSV_Editor:

    @staticmethod
    def clean_house_representative_data_csv(csv_file):
        df = pd.read_csv(csv_file)

        df = CSV_Editor.remove_column(df, 'URL')

        df = CSV_Editor.col_to_str_type(df, 'District', "At Large")

        df = CSV_Editor.convert_state_names_to_abbrev(df, 'State')

        df = CSV_Editor.convert_party_to_initial(df, 'Party')

        df = CSV_Editor.format_names_for_reps_senators(df, 'Name')

        df.to_csv(csv_file, index=False)

    @staticmethod
    def convert_party_to_initial(dataframe, column_key):

        for _, row in dataframe.iterrows():
            if 'Republican' in row[column_key]:
                row[column_key] = 'R'
            elif 'Democrat' in row[column_key]:
                row[column_key] = 'D'
            else:
                row[column_key] = 'I'

        return dataframe

    @staticmethod
    def format_names_for_reps_senators(dataframe, column_key):

        for _, row in dataframe.iterrows():
            string = str(row[column_key])

            comma_count = string.count(',')

            string_split = string.split()

            string_split.remove(string_split[0])

            if comma_count > 1:

                last_name = string_split[0][:-1]
                string_split.remove(string_split[0])
                string_split.insert(-1, last_name)
                for name in string_split:
                    if ',' in name:
                        if '"' in name:
                            temp = name[0:-2] + '"'
                        else:
                            temp = name[:-1]
                        string_split[string_split.index(name)] = temp

            else:
                if len(string_split) == 5:
                    new_list = list()
                    new_list.append(string_split[2])
                    new_list.append(string_split[3])
                    new_list.append(string_split[4])
                    new_list.append(string_split[0])
                    new_list.append(string_split[1][:-1])

                    string_split = new_list.copy()

                if len(string_split) == 4:
                    if 'IV' in string_split:
                        new_list = list()
                        new_list.append(string_split[1])
                        new_list.append(string_split[2])
                        new_list.append(string_split[0][:-1])
                        new_list.append(string_split[3])

                    else:
                        new_list = list()
                        new_list.append(string_split[1])
                        new_list.append(string_split[2])
                        new_list.append(string_split[3])
                        new_list.append(string_split[0][:-1])

                    string_split = new_list.copy()

                if len(string_split) == 3:
                    for part in string_split:
                        if ',' in part and string_split.index(part) == 1:
                            new_list = list()
                            new_list.append(string_split[2])
                            new_list.append(string_split[0])
                            new_list.append(string_split[1][:-1])
                            string_split = new_list.copy()

                        elif ',' in part and string_split.index(part) == 0:
                            new_list = list()
                            new_list.append(string_split[1])
                            new_list.append(string_split[2])
                            new_list.append(string_split[0][:-1])
                            string_split = new_list.copy()

                if len(string_split) == 2:
                    temp = string_split[0][:-1]
                    string_split[0] = string_split[1]
                    string_split[1] = temp

            string = ' '.join(string_split)
            if "\"" in string:
                string.replace("\"", "\'")
            row[column_key] = string
            print(string)

        return dataframe




    @staticmethod
    def print_df_types(dataframe):

        print("Types in dataframe: " + str(dataframe.dtypes))

    @staticmethod
    def col_to_str_type(dataframe, column_key, fill_string):

        dataframe[column_key].fillna(fill_string, inplace=True)

        dataframe = dataframe.astype(str)

        return dataframe

    @staticmethod
    def remove_column(dataframe, column_key):

        print(dataframe.columns.tolist())
        del dataframe[column_key]

        return dataframe

    @staticmethod
    def convert_state_names_to_abbrev(dataframe, column_key):

        for _, row in dataframe.iterrows():
            state = CSV_Editor.stateSelector(row[column_key])
            row[column_key] = state

        return dataframe

    @staticmethod
    def stateSelector(state):
        """
        Utility function that returns zipped list of state abbreviations and state names
        :return: zipped list of state abbrevs and names
        """

        states_abbrev = ['al', 'ak', 'az', 'ar', 'ca', 'co', 'ct', 'dc', 'de', 'fl', 'ga', 'hi', 'id', 'il', 'in',
                         'ia',
                         'ks', 'ky', 'la', 'me', 'md', 'ma', 'mi', 'mn', 'ms', 'mo', 'mt', 'ne', 'nv', 'nh', 'nj',
                         'nm',
                         'ny', 'nc', 'nd', 'oh', 'ok', 'or', 'pa', 'ri', 'sc', 'sd', 'tn', 'tx', 'ut', 'vt', 'va',
                         'wa',
                         'wv', 'wi', 'wy']

        states = ['alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado', 'connecticut',
                  'washington d.c.',
                  'delaware', 'florida', 'georgia', 'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas',
                  'kentucky', 'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota',
                  'mississippi',
                  'missouri', 'montana', 'nebraska', 'nevada', 'new hampshire', 'new jersey', 'new mexico',
                  'new york', 'north carolina', 'north dakota', 'ohio', 'oklahoma', 'oregon', 'pennsylvania',
                  'rhode island', 'south carolina', 'south dakota', 'tennessee', 'texas', 'utah', 'vermont',
                  'virginia', 'washington', 'west virginia', 'wisconsin', 'wyoming']

        states_map = [x for x in zip(states_abbrev, states)]

        for pair in states_map:
            if state.lower() in pair:
                for item in pair:
                    if state.lower() != item:
                        return item.upper()


    @staticmethod
    def clean_bills_names(csv_file, chamber, year):
        if chamber == 'house':
            ref_file = f"../csv_data/house_reps_{year}.csv"
        else:
            ref_file = f"../csv_data/senators_{year}.csv"

        ref_df = pd.read_csv(ref_file)
        names = ref_df['Name']

        bill_file = pd.read_csv(csv_file)

        correct_matches = dict()

        for _, row in bill_file.iterrows():
            name_split = str(row['sponsors']).split()

            new_split = list()
            for part in name_split:
                if 'Rep.' not in part and '[' not in part and ']' not in part:
                    if ',' in part:
                        new_split.append(part[:-1])
                    else:
                        new_split.append(part)
            name_split = new_split.copy()
            print(name_split)
            possible_matches = list()
            for n in names:
                match_count = 0
                for part in name_split:
                    if part in n:
                        match_count += 1
                if match_count > 1:
                    possible_matches.append(n)
            if len(possible_matches) > 1:
                try:
                    correct_name = correct_matches[row['sponsors']]
                    print(f"replacing {row['sponsors']} with {correct_name}")
                    row['sponsors'] = correct_name

                except:
                    for poss in possible_matches:
                        print("correct(?): " + poss)
                        print("to be replaced: " + ' '.join(name_split))
                        answer = input('Replace with correct?\n>')
                        if answer == 'y':

                            correct_matches[row['sponsors']] = poss
                            row['sponsors'] = poss
                            break
            elif len(possible_matches) == 1:
                print(f"replacing {row['sponsors']} with {possible_matches[0]}")
                row['sponsors'] = possible_matches[0]
            else:
                input(f"NO MATCHES FOUND for {' '.join(name_split)}")

        bill_file.to_csv(csv_file, index=False, encoding='utf-8')

    @staticmethod
    def clean_committees_names(csv_file, year):
        house_ref_file = f"../csv_data/house_reps_{year}.csv"
        senate_ref_file = f"../csv_data/senators_{year}.csv"

        house_ref_df = pd.read_csv(house_ref_file)
        senate_ref_df = pd.read_csv(senate_ref_file)
        all_ref_df = pd.concat([house_ref_df, senate_ref_df])
        names = all_ref_df['Name']

        correct_matches = dict()
        committee_file = pd.read_csv(csv_file)

        for _, row in committee_file.iterrows():
            name_split = str(row['Name']).split()
            new_split = list()
            for part in name_split:
                if 'Rep.' not in part and '[' not in part and ']' not in part:
                    if ',' in part:
                        new_split.append(part[:-1])
                    else:
                        new_split.append(part)
            name_split = new_split.copy()
            print(name_split)
            possible_matches = list()

            for n in names:
                match_count = 0
                for part in name_split:
                    if part in n:
                        match_count += 1
                if match_count > 1:
                    possible_matches.append(n)
            if len(possible_matches) > 1:
                try:
                    correct_name = correct_matches[row['Name']]
                    print(f"replacing {row['Name']} with {correct_name}")
                    row['Name'] = correct_name

                except:
                    for poss in possible_matches:
                        print("correct(?): " + poss)
                        print("to be replaced: " + ' '.join(name_split))
                        answer = input('Replace with correct?\n>')
                        if answer == 'y':
                            correct_matches[row['Name']] = poss
                            row['Name'] = poss
                            break
            elif len(possible_matches) == 1:
                print(f"replacing {row['Name']} with {possible_matches[0]}")
                row['Name'] = possible_matches[0]
            else:
                input(f"NO MATCHES FOUND for {' '.join(name_split)}")

        committee_file.to_csv(csv_file, index=False, encoding='utf-8')

    @staticmethod
    def create_roll_call_dictionary(csv_file):
        df = pd.read_csv(csv_file)
        d_wow = dict()
        for _, row in df.iterrows():
            full_name = row['Name']
            last_name = full_name.split()[-1]
            if last_name in d_wow:
                d_wow[last_name][full_name] = row['State']
            else:
                d_wow[last_name] = dict()
                d_wow[last_name][full_name] = row['State']
        return d_wow

    @staticmethod
    def clean_roll_call_member(csv_file, rc_file):
        votes_file = pd.read_csv(rc_file)
        member_dict = CSV_Editor.create_roll_call_dictionary(csv_file)

        for _, row in votes_file.iterrows():
            name_split = str(row['member']).split()
            # party = str(row['party'])
            state = ''
            short_name = ''
            full_name = ''
            if len(name_split) == 0:
                continue
            if len(name_split) == 1:
                short_name = name_split[0]
                print(f"replacing {row['member']} with {name_split[0]}")
                row['member'] = name_split[0]


            #
            #         correct_matches[short_name]: result[0]
            #     if len(result) > 1:
            #         print(result)


            # elif len(name_split) > 1:
            #     for entry in name_split:
            #         if '(' in entry:
            #             state = entry.strip('(')
            #             state = state.strip(')')
            #         else:
            #             long_name = long_name + ' ' + entry
            # print(short_name, long_name, state, party)

            # correct_matches[name] =
            # result = ref_df[(ref_df['Name'].str.contains(short_name)) & (ref_df['State'].str.contains(state))]
            # print(result)
            # print(len(result))
            # if len(result) > 1:
            #     possible_matches = list()
            #     for
            #     try:
            #         print(f"Is this a match for {long_name}?")
            #         print(result)

            #             correct_name = correct_matches[row['member']]
            #             print(f"replacing {row['member']} with {correct_name}")
            #             row['member'] = correct_name
            #
            #         except:
            #             for poss in possible_matches:
            #                 print("correct(?): " + poss)
            #                 print("to be replaced: " + ' '.join(name_split))
            #                 answer = input('Replace with correct?\n>')
            #                 if answer == 'y':
            #                     correct_matches[row['Name']] = poss
            #                     row['member'] = poss
            #                     break

            # print(name_split, party)
            # if len(name_split) == 1:
            #     result = ref_df[ref_df['Name'].str.contains(name_split[0])]
            #     print(result)
            #
            # if len(name_split) > 1:
            #     if '(' in name_split[1]:
            #         state = name_split[1].strip('(')
            #         state = state.strip(')')
            #         state_result = ref_df[ref_df['State'].str.contains(state)]
            #         result = state_result[state_result['Name'].str.contains(name_split[0])]
            #         print(result)
            #     else:
            #         name = name_split[0] + ' ' + name_split[1]
            #         print(f"name: {name}")
            #         result = ref_df[ref_df['Name'].str.contains(name)]
            #         print(result)

            # if len(result) == 1:
            # result = names.str.contains(name_split[0])
            # print(names)
            possible_matches = list()

        #     for n in names:
        #         match_count = 0
        #         for part in name_split:
        #             if part in n:
        #                 match_count += 1
        #         if match_count > 1:
        #             possible_matches.append(n)
        #     if len(possible_matches) > 1:
        #         try:
        #             correct_name = correct_matches[row['member']]
        #             print(f"replacing {row['member']} with {correct_name}")
        #             row['member'] = correct_name
        #
        #         except:
        #             for poss in possible_matches:
        #                 print("correct(?): " + poss)
        #                 print("to be replaced: " + ' '.join(name_split))
        #                 answer = input('Replace with correct?\n>')
        #                 if answer == 'y':
        #                     correct_matches[row['Name']] = poss
        #                     row['member'] = poss
        #                     break
        #     elif len(possible_matches) == 1:
        #         print(f"replacing {row['member']} with {possible_matches[0]}")
        #         row['member'] = possible_matches[0]
        #     else:
        #         input(f"NO MATCHES FOUND for {' '.join(name_split)}")
        #
        # votes_file.to_csv(csv_file, index=False, encoding='utf-8')