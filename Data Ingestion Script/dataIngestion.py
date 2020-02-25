import sys
import psycopg2 as pg
import csv
import pandas as pd


DB_NAME = "REDACTED"
DB_USER = "REDACTED"
DB_PASSWORD = "REDACTED"
DB_HOST = "REDACTED"
DB_PORT = "REDACTED"

try:
    local_echo = False
    with open('credentials.csv', newline='') as csvfile:
        credentializer = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in credentializer:
            DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT = row

    if local_echo == True:
        print("Read in DB Name as - ", DB_NAME)
        print("Read in DB User as - ", DB_USER)
        print("Read in DB Password as - ", DB_PASSWORD)
        print("Read in DB Host as - ", DB_HOST)
        print("Read in DB Port as - ", DB_PORT)

except:
    print("Flagrant Error - credentials.csv file not found!")


def throw_psycopg2_exception(error):
    err_type, err_obj, traceback = sys.exc_info()
    line_num = traceback.tb_lineno

    print("\nPsycopg2 ERROR:", err, "on line number", line_num)
    print("\nPsycopg2 Traceback: ", traceback, " -- type ", err_type)
    print("\nextensions.Diagnostics:", err.diag)
    print("\npgerror:", err.error)
    print("\npgcode:", err.pgcode, "\n")


try:
    connection = pg.connect(database=DB_NAME, user=DB_USER,
                            password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
except pg.OperationalError as err:
    throw_psycopg2_exception(err)


def create_rep_table_115():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS representative_115 (
                rep_name varchar(255) UNIQUE NOT NULL,
                state varchar(255),
                district varchar(255),
                party varchar(255),
                terms varchar(255),
                congress integer,
                PRIMARY KEY (rep_name, congress)
                );
        """)
        curs.execute("""
                ALTER TABLE representative_115 OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - Representative table created for 115th session.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)

def create_rep_table_116():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS representative_116 (
                rep_name varchar(255) UNIQUE NOT NULL,
                state varchar(255),
                district varchar(255),
                party varchar(255),
                terms varchar(255),
                congress integer,
                PRIMARY KEY (rep_name, congress)
                );
        """)
        curs.execute("""
                ALTER TABLE representative_116 OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - Representative table created for 116th session.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)

def create_house_resolution_115():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS house_resolution_115 (
                res_name varchar(255) PRIMARY KEY NOT NULL,
                description varchar(1000),
                status varchar(255),
                committees varchar(255),
                sponsor varchar(255) REFERENCES representative_115(rep_name),
                congress integer
                );
        """)
        curs.execute("""
                ALTER TABLE house_resolution_115 OWNER to postgres
        """)
        connection.commit()
        print("Operation Succeeded - House Resolution table created for 115th session.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_house_resolution_116():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS house_resolution_116 (
                res_name varchar(255) PRIMARY KEY NOT NULL,
                description varchar(1000),
                status varchar(255),
                committees varchar(255),
                sponsor varchar(255) REFERENCES representative_116(rep_name),
                congress integer
                );
        """)
        curs.execute("""
                ALTER TABLE house_resolution_116 OWNER to postgres
        """)
        connection.commit()
        print("Operation Succeeded - House Resolution table created for 116th session.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_house_committee_table_115():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS house_committee_115 (
                hc_name varchar(255) UNIQUE NOT NULL,
                chair varchar(255) NOT NULL REFERENCES representative_115(rep_name),
                ranking_member varchar(255) REFERENCES representative_115(rep_name),
                PRIMARY KEY (hc_name, chair)
                );
        """)
        curs.execute("""
                ALTER TABLE house_committee_115 OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - House Committee table created for 115th session.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_house_committee_table_116():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS house_committee_116 (
                hc_name varchar(255) UNIQUE NOT NULL,
                chair varchar(255) NOT NULL REFERENCES representative_116(rep_name),
                ranking_member varchar(255) REFERENCES representative_116(rep_name),
                PRIMARY KEY (hc_name, chair)
                );
        """)
        curs.execute("""
                ALTER TABLE house_committee_116 OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - House Committee table created for 116th session.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_house_subcommittee_table():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS house_subcommittee (
                hsubc_name varchar(255) NOT NULL,
                sc_of varchar(255) REFERENCES house_committee(hc_name),
                PRIMARY KEY (hsubc_name, sc_of)
                );
        """)
        curs.execute("""
                ALTER TABLE house_subcommittee OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - House Subcommittee table created.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_house_committee_relational_table():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS house_com_rel (
                rep_name varchar(255) REFERENCES representative(rep_name),
                hc_name varchar(255) REFERENCES house_committee(hc_name),
                chair varchar(3),
                ranking_member varchar(3),
                CONSTRAINT CHK_CHAIR CHECK (chair in ('yes', 'no')),
                CONSTRAINT CHK_RNK_MEM CHECK (ranking_member in ('yes', 'no'))
                );
        """)
        curs.execute("""
                ALTER TABLE house_com_rel OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - House Committe Relational table created")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_res_cosponsors_table():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS res_cosponsors (
                res_name varchar(255) NOT NULL REFERENCES house_resolution(res_name),
                cosponsor varchar(255) REFERENCES representative(rep_name),
                PRIMARY KEY (res_name, cosponsor)
                );
        """)
        curs.execute("""
                ALTER TABLE res_cosponsors OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - House Resolution Co-Sponsors")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)

# --------------------------------------------------------------------------------------
'''
Create senate tables
'''


def create_sen_table_115():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS senator_115 (
                sen_name varchar(255) UNIQUE NOT NULL,
                state varchar (255),
                party varchar(255),
                terms varchar(255),
                congress integer,
                PRIMARY KEY (sen_name, state, congress)
                );
        """)
        curs.execute("""
                ALTER TABLE senator_115 OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - Senator table created for 115th session.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)

def create_sen_table_116():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS senator_116 (
                sen_name varchar(255) UNIQUE NOT NULL,
                state varchar (255),
                party varchar(255),
                terms varchar(255),
                congress integer,
                PRIMARY KEY (sen_name, state, congress)
                );
        """)
        curs.execute("""
                ALTER TABLE senator_116 OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - Senator table created for 116th session.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_senate_bill_table():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS senate_bill(
                bill_name varchar(255) UNIQUE PRIMARY KEY NOT NULL,
                sponsor varchar(255) REFERENCES senator(sen_name),
                committees varchar(255),
                bill_status varchar(255),
                description varchar(500)
                );
        """)
        curs.execute("""
                ALTER TABLE senate_bill OWNER to postgres
        """)
        connection.commit()
        print("Operation succeeded - Senate Bill table created")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_senate_committee_table():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS senate_committee (
                sc_name varchar(255) NOT NULL,
                chair varchar(255) NOT NULL REFERENCES senator(sen_name),
                ranking_member varchar(255) REFERENCES senator(sen_name),
                PRIMARY KEY (sc_name, chair)
                );
        """)
        curs.execute("""
                ALTER TABLE senate_committee OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - Senate Committee table created.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_senate_subcommittee_table():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS senate_subcommittee (
                ssubc_name varchar(255) NOT NULL,
                sc_of varchar(255) REFERENCES senate_committee(sc_name),
                PRIMARY KEY (ssubc_name, sc_of)
                );
        """)
        curs.execute("""
                ALTER TABLE senate_subcommittee OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - Senate Subcommittee table created.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_senate_com_rel_table():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS senate_com_rel (
                sen_name varchar(255) REFERENCES senator(sen_name),
                sc_name varchar(255) REFERENCES senate_committee(sc_name),
                chair varchar(3),
                ranking_member varchar(3),
                CONSTRAINT CHK_CHAIR CHECK (chair in('yes', 'no')),
                CONSTRAINT CHK_RNK_MEM CHECK (ranking_member in ('yes', 'no'))
                );
        """)
        curs.execute("""
                ALTER TABLE senate_com_rel OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - Senate Committee Relational table created")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_sen_bill_cosponsors_table():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS bill_cosponsors (
                bill_name varchar(255) NOT NULL REFERENCES senate_bill(bill_name),
                cosponsor varchar(255) NOT NULL REFERENCES senator(sen_name),
                PRIMARY KEY (bill_name, cosponsor)
        );
        """)
        curs.execute("""
                ALTER TABLE bill_cosponsors OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - Senate Bill Co-Sponsors table created")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)

# --------------------------------------------------------------------------------------
'''
Representative insertion functions and their associated cleanup functions
DO NOT RUN fix_reps functions on files which are already fixed - You can tell if
    a file has been fixed because the district will be an integer, rather than a
    float, or At Large will have been replaced with 'At Large'.
    
Running it on fixed files will produce an index out of range error and a crash.
Although this is fixable, an easier solution is to don't run it twice on the same
file.
'''


def fix_reps_115_csv():
    reps = csv.reader(open('..\webscraping\csv_data\house_reps_115.csv'))
    lines = list(reps)

    for line in lines:
        print(line)
        if line[0] == 'Madeleine Z. Bordallo':
            line[1] = 'GU'
        elif line[0] == 'Jenniffer Gonzalez-Colon':
            line[1] = 'PR'
        elif line[0] == 'Eleanor Holmes Norton':
            line[1] = 'DC'
        elif line[0] == 'Stacey E. Plaskett':
            line[1] = 'VI'
        elif line[0] == 'Aumua Amata Coleman Radewagen':
            line[1] = 'AS'
        elif line[0] == 'Gregorio Kilili Camacho Sablan':
            line[1] = 'MP'
        elif line[0] == 'Tom O\'Halleran':
            line[0] = 'Tom O''Halleran'
        elif line[0] == 'Beto O\'Rourke':
            line[0] = 'Beto O''Rourke'
        else:
            pass

    for line in lines:
        print(line)
        if line[2] == 'At Large':
            line[2] = '\'At Large\''
        elif line[2] != 'District':
            line[2] = ''.join(line[2].split())[:-2]
        print(line[2])

    writer = csv.writer(open('..\webscraping\csv_data\house_reps_115.csv', 'w'))
    writer.writerows(lines)


def fix_reps_116_csv():
    reps = csv.reader(open('..\webscraping\csv_data\house_reps_116.csv'))
    lines = list(reps)

    for line in lines:
        print(line)
        if line[0] == 'Michael F. Q. San Nicolas':
            line[1] = 'GU'
        elif line[0] == 'Jenniffer Gonzalez-Colon':
            line[1] = 'PR'
        elif line[0] == 'Eleanor Holmes Norton':
            line[1] = 'DC'
        elif line[0] == 'Stacey E. Plaskett':
            line[1] = 'VI'
        elif line[0] == 'Aumua Amata Coleman Radewagen':
            line[1] = 'AS'
        elif line[0] == 'Gregorio Kilili Camacho Sablan':
            line[1] = 'MP'
        elif line[0] == 'Tom O\'Halleran':
            line[0] = 'Tom O''Halleran'
        elif line[0] == 'Beto O\'Rourke':
            line[0] = 'Beto O''Rourke'
        else:
            pass

    for line in lines:
        print(line)
        if line[2] == 'At Large':
            line[2] = '\'At Large\''
        elif line[2] != 'District':
            line[2] = ''.join(line[2].split())[:-2]
        print(line[2])

    writer = csv.writer(open('..\webscraping\csv_data\house_reps_116.csv', 'w'))
    writer.writerows(lines)


def insert_reps_115():
    try:
        reps = pd.read_csv('..\webscraping\csv_data\house_reps_115.csv')
        curs = connection.cursor()
        print("Loading Data from house_reps_115.csv")
        for index, row in reps.iterrows():
            print("Inserting row", row["Name"])
            curs.execute("""
            INSERT into representative_115(rep_name, state, district, party, terms, congress)
            VALUES (
                '%s', '%s', %s, '%s', '%s', 115
            )""" % (row['Name'].strip(), row['State'].strip(), row['District'], row['Party'].strip(),
                    row['Terms'].strip())
                         )

        connection.commit()
        print("Data from Representative.csv successfully inserted.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def insert_reps_116():
    try:
        reps = pd.read_csv('..\webscraping\csv_data\house_reps_116.csv')
        curs = connection.cursor()
        print("Loading Data from house_reps_116.csv")
        for index, row in reps.iterrows():
            print("Inserting row", row["Name"])
            curs.execute("""
            INSERT into representative_116(rep_name, state, district, party, terms, congress)
            VALUES (
                '%s', '%s', %s, '%s', '%s', 116
            )""" % (row['Name'].strip(), row['State'].strip(), row['District'], row['Party'].strip(), row['Terms'].strip())
            )

        connection.commit()
        print("Data from Representative.csv successfully inserted.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)

# --------------------------------------------------------------------------------------


def insert_house_resolutions_115():
    try:
        bills = pd.read_csv('..\webscraping\csv_data\house_bills_115.csv')
        reps = pd.read_csv('..\webscraping\csv_data\house_reps_115.csv')

        rep_names = reps['Name'].tolist()

        curs = connection.cursor()
        print("Loading Data from house_resolutions_115.csv")
        for index, row in bills.iterrows():
            print("Row[names] is", row['names'], "and type is", type(row['names']))
            print("Row[descriptions] is", row['descriptions'], "and type is", type(row['descriptions']))
            print("Row[statuses] is", row['statuses'], "and type is", type(row['statuses']))
            print("Row[bill_committees] is", row['bill_committees'], "and type is", type(row['bill_committees']))
            print("Row[sponsors] is", row['sponsors'], "and type is", type(row['sponsors']))
            if row['sponsors'] in rep_names:
                curs.execute("""
                INSERT into house_resolution_115(res_name, sponsor, committees, status, description, congress)
                VALUES
                (
                '%s', '%s', '%s', '%s', '%s', 115)
                """ % (row['names'].strip(), row['descriptions'].strip(), row['statuses'].strip(), row['bill_committees'].strip(), row['sponsors'].strip()))
        connection.commit()
        print("Data from house_resolutions_115.csv successfully inserted")

    except pg.OperationalError as err:
        throw_psycopg2_exception(err)

def insert_house_committee():
    try:
        subc = pd.read_csv('house_subcommittee.csvc')

        curs = connection.cursor()

        house_committees = ["Agriculture", "Appropriations", "Armed Services", "Budget", "Education and Labor",
                            "Energy and Commerce", "Ethics", "Financial Services", "Foreign Affairs", "Homeland Security",
                            "House Administration", "Judiciary", "Natural Resources", "Oversight and Reform", "Rules",
                            "Science, Space, and Technology", "Small Business", "Transportation and Infrastructure",
                            "Veterans Affairs", "Ways and Means", "Permanent Select Committee on Intelligence",
                            "Select Committee on the Climate Crisis", "Select Committee on the Modernization of Congress"]

        senate_committees = ["Agriculture, Nutrition, and Forestry", "Appropriations", "Armed Services",
                             "Banking, Housing, and Urban Affairs", "Budget", "Commerce, Science, and Transportation",
                             "Energy and Natural Resources", "Environment and Public Works", "Finance",
                             "Foreign Relations",
                             "Health, Education, Labor, and Pensions", "Homeland Security and Governmental Affairs",
                             "Judiciary", "Rules and Administration", "Small Business and Entrepreneurship",
                             "Veterans Affairs", "Aging", "Ethics", "Indian Affairs", "Intelligence",
                             "Senate Narcotics Caucus"]

        for committee in house_committees:
            curs.execute("""
            INSERT INTO congress.house_committee(hc_name)
            VALUES
            (
            '%s'
            )""" %(committee))

        for committee in senate_committees:
            curs.execute("""
            INSERT INTO congress.senate_committee(sc_name)
            VALUES
            (
            
            '%s'
            )""" %(committee))

        connection.commit()
        print('Committee and Subcommittee values added to tables')

    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def add_committee_members_and_subcommitees_tables():
    try:
        curs = connection.cursor()

        committee_members = pd.read_csv('committee_members.csv')
        subcommittees = pd.read_csv('subcommittes.csv')
        for index, row in committee_members.iterrows():
            if '"' in row ['hcname']:
                row['hcname'] = row['hcname'][1:-1]

            curs.execute("""
            INSERT INTO congress.house_com_rel(rep_name, hc_name, chair, ranking_member)
            VALUES
            (
            '%s', '%s', 'no', 'no'
            )
            """ % (row['rname'], row['hcname']))  # need to insert yes/no for chair and ranking member

            for index, row in subcommittees.iterrows():

                if '"' in row['hsubc_name']:
                    row['hsubc_name'] = row['hsubc_name'][1:-1]

                if '"' in row['hc_name']:
                    row['hc_name'] = row['hc_name'][1:-1]

                curs.execute("""
                INSERT INTO congress.house_subcommittee (hsubc_name, sc_of)
                VALUES
                (
                '%s', '%s'
                )
                """ % (row['hsubc_name'], row['hc_name']))
            connection.commit()
            print("Committee Members and Subcommittees Added to Tables")

    except pg.OperationalError as err:
        throw_psycopg2_exception(err)

# --------------------------------------------------------------------------------------
'''
Senate Insertion script functions - there aren't any supplementary cleanup functions for
these functions.
'''

def insert_sen_115():
    try:
        reps = pd.read_csv('..\webscraping\csv_data\senators_115.csv')
        curs = connection.cursor()
        print("Loading Data from house_reps_116.csv")
        for index, row in reps.iterrows():
            print("Inserting row", row["Name"])
            curs.execute("""
            INSERT into senator_115(sen_name, state, party, terms, congress)
            VALUES (
                '%s', '%s', '%s', '%s', 116
            )""" % (row['Name'].strip(), row['State'].strip(), row['Party'].strip(), row['Terms'].strip())
            )

        connection.commit()
        print("Data from Senators_115.csv successfully inserted.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def insert_sen_116():
    try:
        reps = pd.read_csv('..\webscraping\csv_data\senators_116.csv')
        curs = connection.cursor()
        print("Loading Data from house_reps_116.csv")
        for index, row in reps.iterrows():
            print("Inserting row", row["Name"])
            curs.execute("""
            INSERT into senator_116(sen_name, state, party, terms, congress)
            VALUES (
                '%s', '%s', '%s', '%s', 116
            )""" % (row['Name'].strip(), row['State'].strip(), row['Party'].strip(), row['Terms'].strip())
            )

        connection.commit()
        print("Data from Senators_116.csv successfully inserted.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)

# --------------------------------------------------------------------------------------

# create_rep_table_115()                        # Created
# create_rep_table_116()                        # Created
# create_house_committee_table_115()            # Created
# create_house_committee_table_116()            # Created
create_house_resolution_115()                 # Created
create_house_resolution_116()                 # Created
# create_house_subcommittee_table()             # Not Created
# create_house_committee_relational_table()     # Not Created

# create_sen_table_115()                        # Created
# create_sen_table_116()                        # Created
# create_senate_bill_table()                    # Not Created
# create_senate_committee_table()               # Not Created
# create_senate_subcommittee_table()            # Not Created
# create_senate_com_rel_table()                 # Not Created
# create_sen_bill_cosponsors_table()            # Not Created

# fix_reps_115_csv()                            # Executed
# fix_reps_116_csv()                            # Executed
# insert_reps_115()                             # Executed
# insert_reps_116()                             # Executed
insert_house_resolutions_115()
# insert_house_bills_116()
# insert_house_committee()

# insert_sen_115()                              # Executed
# insert_sen_116()                              # Executed