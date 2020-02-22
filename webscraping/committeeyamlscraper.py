import yaml


def parse_committee_yaml(file_path):
    """
    :param file_path: committee assignment yaml file to parse
    :return: dictionary that maps committee and subcommittee short name (i.e. 'thomas id') to membership list of rep / senator names
             dictionary that maps committee and subcommittee short name (i.e. 'thomas id') to leadership list of tuples (name, position)
    """
    with open(file_path, mode='r') as file:
        committees_list = yaml.load(file, Loader=yaml.FullLoader)

        committee_dict = dict()
        committee_leadership_dict = dict()

        for committee_name, value in committees_list.items():
            committee_dict[committee_name] = []
            committee_leadership_dict[committee_name] = []
            for item in value:
                name = ''
                for k, v in item.items():
                    if k == 'name':
                        committee_dict[committee_name].append(v)
                        name = v
                    if k == 'title':
                        committee_leadership_dict[committee_name].append((name, v))

        return committee_dict, committee_leadership_dict


def map_committee_name(file_path):
    """
    :param file_path: committee info yaml to parse
    :return: a dictionary that maps thomas id to committee and subcommittee name
    """
    with open(file_path, mode='r') as file:
        committees_list = yaml.load(file, Loader=yaml.FullLoader)
    committee_name_map = dict()

    for committee in committees_list:
        key = committee["thomas_id"]
        value = committee["name"]
        committee_name_map[key] = []
        committee_name_map[key].append(value)

        if "subcommittees" in committee.keys():
            for subcommittee in committee["subcommittees"]:
                k = (committee["thomas_id"] + subcommittee["thomas_id"])
                v = committee["name"] + " - " + subcommittee["name"]
                committee_name_map[k] = []
                committee_name_map[k].append(v)

    return committee_name_map


committee_dict_115, committee_leadership_dict_115 = parse_committee_yaml('yaml/115_committee_assignments.yaml')
committee_dict_116, committee_leadership_dict_116 = parse_committee_yaml('yaml/116_committee_assignments.yaml')
committee_name_map_dict = map_committee_name('yaml/committees.yaml')

# print(committee_dict_115)
# print(committee_leadership_dict_115)
# print(committee_name_map_dict)
