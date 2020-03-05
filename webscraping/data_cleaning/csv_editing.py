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
        d_full_name = dict()
        d_state = dict()
        for _, row in df.iterrows():
            full_name = row['Name']
            if full_name.split()[-1] == 'Jr.':
                last_name = full_name.split()[-2]
            elif full_name.split()[-1] == 'III':
                last_name = full_name.split()[-2]
            elif full_name.split()[-1] == 'IV':
                last_name = full_name.split()[-2]
            elif full_name.split()[-2] + ' ' + full_name.split()[-1] == 'Jackson Lee':
                last_name = 'Jackson Lee'
            elif full_name.split()[-2] + ' ' + full_name.split()[-1] == 'Herrera Beutler':
                last_name = 'Herrera Beutler'
            elif full_name.split()[-2] + ' ' + full_name.split()[-1] == 'McMorris Rodgers':
                last_name = 'McMorris Rodgers'
            elif full_name.split()[-2] + ' ' + full_name.split()[-1] == 'Blunt Rochester':
                last_name = 'Blunt Rochester'
            elif full_name == 'Francis Rooney':
                last_name = 'Rooney Francis'
            elif full_name == 'Thomas J. Rooney':
                last_name = 'Rooney Thomas J.'
            elif full_name == 'Al Green':
                last_name = 'Green Al'
            elif full_name == 'Gene Green':
                last_name = 'Green Gene'
            elif full_name == 'Eddie Bernice Johnson':
                last_name =  'Johnson E. B.'
            elif full_name == 'Sam Johnson':
                last_name = 'Johnson Sam'
            elif full_name == 'Michael F. Doyle':
                last_name = 'Doyle Michael F.'
            elif full_name == 'Michelle Lujan Grisham':
                last_name = 'Lujan Grisham M.'
            elif full_name == 'Ben Ray Lujan':
                last_name = 'Lujan Ben Ray'
            elif full_name == 'Ted Lieu':
                last_name = 'Lieu Ted'
            elif full_name == 'Kendra S. Horn':
                last_name = 'Horn Kendra S'
            elif full_name == 'Mimi Walters':
                last_name = 'Walters Mimi'
            elif full_name == 'Brendan F. Boyle':
                last_name = 'Boyle Brendan F.'
            elif full_name == 'Judy Chu':
                last_name = 'Chu Judy'
            elif full_name == 'Danny K. Davis':
                last_name = 'Davis Danny'
            elif full_name == 'Rodney Davis':
                last_name = 'Davis Rodney'
            elif full_name == 'Jody B. Hice':
                last_name = 'Hice Jody B.'
            elif full_name == 'Carolyn B. Maloney':
                last_name = 'Maloney Carolyn B.'
            elif full_name == 'Sean Patrick Maloney':
                last_name = 'Maloney Sean'
            elif full_name == 'Austin Scott':
                last_name = 'Scott Austin'
            elif full_name == 'David Scott':
                last_name = 'Scott David'
            elif full_name == 'Debbie Wasserman Schultz':
                last_name = 'Wasserman Schultz'
            elif full_name == 'Bonnie Watson Coleman':
                last_name = 'Watson Coleman'
            elif full_name == 'Randy K. Weber Sr.':
                last_name = 'Weber'
            elif full_name == 'Maxine Waters':
                last_name = 'Waters Maxine'
            elif full_name == 'Kevin Hern':
                last_name = 'Hern Kevin'
            elif full_name == 'David P. Roe':
                last_name = 'Roe David P.'
            elif full_name == 'John W. Rose':
                last_name = 'Rose John W.'
            elif full_name == 'Jefferson Van Drew':
                last_name = 'Van Drew'
            elif full_name == 'Michael F. Q. San Nicolas':
                last_name = 'San Nicolas'
            elif full_name == 'Tom OHalleran':
                last_name = "O\'Halleran"
            elif full_name == 'Beto ORourke':
                last_name = "O\'Rourke"
            else:
                last_name = full_name.split()[-1]

            d_full_name[last_name] = full_name
            d_state[last_name + ' (' + row['State'] + ')'] = full_name
        print(d_full_name)
        return d_full_name, d_state

    @staticmethod
    def clean_roll_call_member(member_file, csv_file):
        votes_file = pd.read_csv(csv_file)
        member_dict, member_state_dict = CSV_Editor.create_roll_call_dictionary(member_file)

        for _, row in votes_file.iterrows():
            member_name = str(row['member'])

            if member_name == '':
                continue
            if member_name == 'nan':
                continue
            if member_name[0] == ' ':
                member_name = member_name[1:]
                print(member_name)

            if "\'" in member_name:
                print(member_name)

            # This one is weird - Walter B. Jones is 'Jones' in roll call
            # until Brenda Jones replaced John Conyers mid-term...
            # Thereafter it's either Jones (MI) or Jones (NC). This
            # needs to be handled, and I don't have more elegant solution
            elif member_name == 'Jones':
                key_name = 'Walter B. Jones Jr.'
            # Suddenly she's just 'Beutler'
            elif member_name == 'Beutler':
                key_name = 'Jaime Herrera Beutler'
            # Of course, because Tom Price...
            elif member_name == 'Price Tom (GA)':
                key_name = 'Tom Price'
            # Ugh
            elif member_name == 'Davis Danny K.':
                key_name = 'Danny K. Davis'
            elif member_name == 'Hice (GA)':
                key_name = 'Jody B. Hice'
            elif member_name == 'Horn Kendra S.':
                key_name = 'Kendra S. Horn'
            elif member_name == 'Johnson (TX)':
                key_name = 'Eddie Bernice Johnson'
            elif member_name == 'Lujan':
                key_name = 'Ben Ray Lujan'
            elif member_name == 'Rodgers (WA)':
                key_name = 'Cathy McMorris Rodgers'
            elif member_name == 'Rooney (FL)':
                key_name = 'Francis Rooney'
            elif member_name == 'Torres Small (NM)':
                key_name = 'Xochitl Torres Small'
            elif member_name == "Waters":
                key_name = 'Maxine Waters'
            elif member_name == 'Green (TX)':
                key_name = 'Al Green'
            elif member_name == "O'Halleran":
                key_name = 'Tom OHalleran'
            elif member_name == 'Roe (TN)':
                key_name = "David P. Roe"
            elif '(' in member_name:
                key_name = member_state_dict[member_name]
            else:
                key_name = member_dict[member_name]

            print(f"replacing {row['member']} with {key_name}")
            row['member'] = key_name

        # votes_file.to_csv(csv_file, index=False, encoding='utf-8')
