import yaml


def parse_committee_yaml(file_path):
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

        # print(committee_dict)
        # print(committee_leadership_dict)

        return committee_dict, committee_leadership_dict


committee_dict_115, committee_leadership_dict_115 = parse_committee_yaml('yaml/115_subcommittees.yaml')
committee_dict_116, committee_leadership_dict_116 = parse_committee_yaml('yaml/116_subcommittees.yaml')

# this is what each entry looks like:
# 'HLIG08' : [{'name': 'Eric Swalwell', 'party': 'majority', 'rank': 1, 'title': 'Chair', 'bioguide': 'S001193'}...]

"""
Committee acronyms to map to committee names:
HLIG
HSAG
HSAG03
HSAG14
HSAG15
HSAG16
HSAG22
HSAG29
HSAP
HSAP01
HSAP02
HSAP04
HSAP06
HSAP07
HSAP10
HSAP15
HSAP18
HSAP19
HSAP20
HSAP23
HSAP24
HSAS
HSAS02
HSAS03
HSAS25
HSAS26
HSAS28
HSAS29
HSBA
HSBA04
HSBA09
HSBA15
HSBA16
HSBA20
HSBU
HSED
HSED02
HSED10
HSED13
HSED14
HSFA
HSFA05
HSFA07
HSFA13
HSFA14
HSFA16
HSFA17
HSGO
HSGO06
HSGO24
HSGO28
HSHA
HSHA01
HSHM
HSHM05
HSHM07
HSHM08
HSHM09
HSHM11
HSHM12
HSIF
HSIF02
HSIF03
HSIF14
HSIF16
HSIF17
HSIF18
HSII
HSII06
HSII10
HSII13
HSII15
HSII24
HSJU
HSJU01
HSJU03
HSJU05
HSJU08
HSJU10
HSPW
HSPW02
HSPW05
HSPW07
HSPW12
HSPW13
HSPW14
HSRU
HSSM
HSSM23
HSSM24
HSSM25
HSSM27
HSSO
HSSY
HSSY15
HSSY16
HSSY18
HSSY20
HSSY21
HSVR
HSVR03
HSVR08
HSVR09
HSVR10
HSVR11
HSWM
HSWM01
HSWM02
HSWM03
HSWM04
HSWM05
HSWM06
JCSE
JSEC
JSLC
JSPR
JSTX
SCNC
SLET
SLIA
SLIN
SPAG
SSAF
SSAF13
SSAF14
SSAF15
SSAF16
SSAF17
SSAP
SSAP01
SSAP02
SSAP08
SSAP14
SSAP16
SSAP17
SSAP18
SSAP19
SSAP20
SSAP22
SSAP23
SSAP24
SSAS
SSAS13
SSAS14
SSAS15
SSAS16
SSAS17
SSAS20
SSAS21
SSBK
SSBK04
SSBK05
SSBK08
SSBK09
SSBK12
SSBU
SSCM
SSCM28
SSCM29
SSCM30
SSCM32
SSCM26
SSEG
SSEG01
SSEG03
SSEG04
SSEG07
SSEV
SSEV08
SSEV09
SSEV10
SSEV15
SSFI
SSFI02
SSFI10
SSFI11
SSFI12
SSFI13
SSFI14
SSFR
SSFR01
SSFR02
SSFR06
SSFR07
SSFR09
SSFR14
SSFR15
SSGA
SSGA01
SSGA18
SSGA19
SSHR
SSHR09
SSHR11
SSHR12
SSJU
SSJU01
SSJU04
SSJU21
SSJU22
SSJU25
SSRA
SSSB
SSVA
HSCN
HSMH
HSED07
HSBA13
HSHA08
HSGO02
HSGO05
HSRU05
HLIG06
HLIG10
SSCM31
SSJU26
HSBA01
HSRU02
HSRU04
HSSM26
HLIG05
HLIG08
"""