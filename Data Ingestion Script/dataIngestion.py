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
                committees varchar(1000),
                sponsor varchar(255) REFERENCES representative_115 (rep_name),
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
                committees varchar(1000),
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


def create_house_subcommittee_table_115():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS house_subcommittee_115 (
                hsubc_name varchar(255) UNIQUE,
                sc_of varchar(255) REFERENCES house_committee_115(hc_name),
                chair varchar(255) REFERENCES representative_115(rep_name),
                PRIMARY KEY (hsubc_name, sc_of)
                );
        """)
        curs.execute("""
                ALTER TABLE house_subcommittee_115 OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - House Subcommittee table created for 115th session.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_house_subcommittee_table_116():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS house_subcommittee_116 (
                hsubc_name varchar(255) UNIQUE,
                sc_of varchar(255) REFERENCES house_committee_116(hc_name),
                chair varchar(255) REFERENCES representative_116(rep_name),
                PRIMARY KEY (hsubc_name, sc_of)
                );
        """)
        curs.execute("""
                ALTER TABLE house_subcommittee_116 OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - House Subcommittee table created for 116th session.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


# --------------------------------------------------------------------------------------


def create_house_roll_call_115():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS house_roll_call_115 (
                session integer,
                roll_num varchar(255) NOT NULL,
                date varchar(255) NOT NULL,
                issue varchar(255),
                question varchar(255),
                result varchar(255),
                title varchar(1000),
                PRIMARY KEY (roll_num, date)
                );
        """)
        connection.commit()
        print("Operation Succeeded - House Roll Call 115th session table created!")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_house_roll_call_116():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS house_roll_call_116 (
                session integer,
                roll_num varchar(255) NOT NULL,
                date varchar(255) NOT NULL,
                issue varchar(255),
                question varchar(255),
                result varchar(255),
                title varchar(1000),
                PRIMARY KEY (roll_num, date)
                );
        """)
        connection.commit()
        print("Operation Succeeded - House Roll 116th session table created!")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)

# --------------------------------------------------------------------------------------


def create_house_votes_115_table():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS house_votes_115 (
                vote_id integer DEFAULT NEXTVAL('house_votes_115_id_seq'),
                session integer NOT NULL,
                res_name varchar(255) NOT NULL,
                member varchar(255) REFERENCES representative_115(rep_name),
                party varchar(255),
                vote varchar (255),
                PRIMARY KEY (vote_id)
                );
        """)
        connection.commit()
        print("Operation Succeeded - House Votes 115th session table created!")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_house_votes_116_table():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS house_votes_116 (
                vote_id integer DEFAULT NEXTVAL('house_votes_116_id_seq'),
                session integer NOT NULL,
                res_name varchar(255) NOT NULL,
                member varchar(255) REFERENCES representative_116(rep_name),
                party varchar(255),
                vote varchar (255),
                PRIMARY KEY (vote_id)
                );
        """)
        connection.commit()
        print("Operation Succeeded - House Votes 116th session table created!")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)

# --------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------
'''
Create house committee relational table
'''


def create_house_com_rel_table_115():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS house_com_rel_115 (
                rep_name varchar(255) REFERENCES representative_115(rep_name),
                hc_name varchar(255) REFERENCES house_committee_115(hc_name),
                hsubc_name varchar(255) REFERENCES house_subcommittee_115(hsubc_name),
                title varchar(255),
                PRIMARY KEY (rep_name, hc_name, hsubc_name)
                );
        """)
        curs.execute("""
                ALTER TABLE house_com_rel_115 OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - House Committee Relational table created")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_house_com_rel_table_116():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS house_com_rel_116 (
                rep_name varchar(255) REFERENCES representative_116(rep_name),
                hc_name varchar(255) REFERENCES house_committee_116(hc_name),
                hsubc_name varchar(255) REFERENCES house_subcommittee_116(hsubc_name),
                title varchar(255),
                PRIMARY KEY (rep_name, hc_name)
                );
        """)
        curs.execute("""
                ALTER TABLE house_com_rel_116 OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - House Committee Relational table created")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


# --------------------------------------------------------------------------------------
'''
Create resolutions cosponsors table
'''


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


def create_senate_bill_table_115():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS senate_bill_115(
                bill_name varchar(255) UNIQUE PRIMARY KEY NOT NULL,
                description varchar(1000),
                bill_status varchar(255),
                committees varchar(1000),
                sponsor varchar(255) REFERENCES senator_115(sen_name),
                congress integer
                );
        """)
        curs.execute("""
                ALTER TABLE senate_bill_115 OWNER to postgres
        """)
        connection.commit()
        print("Operation succeeded - Senate Bill table for 115th session created")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_senate_bill_table_116():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS senate_bill_116(
                bill_name varchar(255) UNIQUE PRIMARY KEY NOT NULL,
                description varchar(1000),
                bill_status varchar(255),
                committees varchar(1000),
                sponsor varchar(255) REFERENCES senator_116(sen_name),
                congress integer
                );
        """)
        curs.execute("""
                ALTER TABLE senate_bill_116 OWNER to postgres
        """)
        connection.commit()
        print("Operation succeeded - Senate Bill table for 116th session created")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_senate_committee_table_115():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS senate_committee_115 (
                sc_name varchar(255) UNIQUE NOT NULL,
                chair varchar(255) NOT NULL REFERENCES senator_115(sen_name),
                PRIMARY KEY (sc_name, chair)
                );
        """)
        curs.execute("""
                ALTER TABLE senate_committee_115 OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - Senate Committee table for 115th session created.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_senate_committee_table_116():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS senate_committee_116 (
                sc_name varchar(255) UNIQUE NOT NULL,
                chair varchar(255) NOT NULL REFERENCES senator_116(sen_name),
                PRIMARY KEY (sc_name, chair)
                );
        """)
        curs.execute("""
                ALTER TABLE senate_committee_116 OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - Senate Committee table for 116th session created.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_senate_subcommittee_table_115():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS senate_subcommittee_115 (
                ssubc_name varchar(255) UNIQUE NOT NULL,
                sc_of varchar(255) REFERENCES senate_committee_115(sc_name),
                chair varchar(255) REFERENCES senator_115(sen_name),
                PRIMARY KEY (ssubc_name)
                );
        """)
        curs.execute("""
                ALTER TABLE senate_subcommittee_115 OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - Senate Subcommittee table for 115th session created.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_senate_subcommittee_table_116():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS senate_subcommittee_116 (
                ssubc_name varchar(255) UNIQUE NOT NULL,
                sc_of varchar(255) REFERENCES senate_committee_116(sc_name),
                chair varchar(255) REFERENCES senator_115(sen_name),
                PRIMARY KEY (ssubc_name)
                );
        """)
        curs.execute("""
                ALTER TABLE senate_subcommittee_116 OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - Senate Subcommittee table for 116th session created.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)

# --------------------------------------------------------------------------------------
'''
Create senate com rel tables
'''


def create_senate_com_rel_table_115():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS senate_com_rel_115 (
                sen_name varchar(255) REFERENCES senator_115(sen_name),
                sc_name varchar(255) REFERENCES senate_committee_115(sc_name),
                ssubc_name varchar(255) REFERENCES senate_subcommittee_115(ssubc_name),
                title varchar(255)
                );
        """)
        curs.execute("""
                ALTER TABLE senate_com_rel_115 OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - Senate Committee Relational table for session 115 created")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_senate_com_rel_table_116():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS senate_com_rel_116 (
                sen_name varchar(255) REFERENCES senator_116(sen_name),
                sc_name varchar(255) REFERENCES senate_committee_116(sc_name),
                Ssubc_name varchar(255) REFERENCES senate_subcommittee_116(ssubc_name),
                title varchar(255)
                );
        """)
        curs.execute("""
                ALTER TABLE senate_com_rel_116 OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - Senate Committee Relational table for 116th session created")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


# --------------------------------------------------------------------------------------
'''
Create Senate Bill Cosponsors Tables
'''

def create_sen_bill_cosponsors_table_115():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS bill_cosponsors (
                bill_name varchar(255) NOT NULL REFERENCES senate_bill_115(bill_name),
                cosponsor varchar(255) NOT NULL REFERENCES senator_115(sen_name),
                PRIMARY KEY (bill_name, cosponsor)
        );
        """)
        curs.execute("""
                ALTER TABLE bill_cosponsors OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - Senate Bill Co-Sponsors table for 115th session created")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_sen_bill_cosponsors_table_116():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE IF NOT EXISTS bill_cosponsors (
                bill_name varchar(255) NOT NULL REFERENCES senate_bill_116(bill_name),
                cosponsor varchar(255) NOT NULL REFERENCES senator_116(sen_name),
                PRIMARY KEY (bill_name, cosponsor)
        );
        """)
        curs.execute("""
                ALTER TABLE bill_cosponsors OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - Senate Bill Co-Sponsors table for 116th session created")
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
'''
Functions to insert the house_resolutions into the resolutions tables.
'''


def insert_house_resolutions_115():
    try:
        bills = pd.read_csv('..\webscraping\csv_data\house_bills_115.csv')
        reps = pd.read_csv('..\webscraping\csv_data\house_reps_115.csv')

        rep_names = reps['Name'].tolist()

        curs = connection.cursor()
        print("Loading Data from house_resolutions_115.csv")
        for index, row in bills.iterrows():
            if row['sponsors'] in rep_names:
                curs.execute("""
                INSERT into house_resolution_115(res_name, description, status, committees, sponsor, congress)
                VALUES
                (
                '%s', '%s', '%s', '%s', '%s', 115)
                """ % (row['names'].strip(), row['descriptions'].strip(), row['statuses'].strip(),
                       row['bill_committees'].strip(), row['sponsors'].strip())
                )
        connection.commit()
        print("Data from house_resolutions_115.csv successfully inserted")

    except pg.OperationalError as err:
        throw_psycopg2_exception(err)

def insert_house_resolutions_116():
    try:
        bills = pd.read_csv('..\webscraping\csv_data\house_bills_116.csv')
        reps = pd.read_csv('..\webscraping\csv_data\house_reps_116.csv')

        rep_names = reps['Name'].tolist()

        curs = connection.cursor()
        print("Loading Data from house_resolutions_116.csv")
        for index, row in bills.iterrows():
            if row['sponsors'] in rep_names:
                curs.execute("""
                INSERT into house_resolution_116(res_name, description, status, committees, sponsor, congress)
                VALUES
                (
                '%s', '%s', '%s', '%s', '%s', 116)
                """ % (row['names'].strip(), row['descriptions'].strip(), row['statuses'].strip(),
                       row['bill_committees'].strip(), row['sponsors'].strip())
                )
        connection.commit()
        print("Data from house_resolutions_116.csv successfully inserted")

    except pg.OperationalError as err:
        throw_psycopg2_exception(err)

# --------------------------------------------------------------------------------------

def insert_house_committee_115():
    try:
        curs = connection.cursor()

        committees = pd.read_csv('..\webscraping\csv_data\\house_committee_membership_115.csv')
        for index, row in committees.iterrows():
            if row[1] not in (None, ""):
                if '"' in row['Committee']:
                    row['Committee'] = row['Committee'][1:-1]
                if row['Title'] == 'Chair':
                    curs.execute("""
                    INSERT INTO house_committee_115(hc_name, chair)
                    VALUES
                    (
                    '%s', '%s'
                    )
                    ON CONFLICT DO NOTHING
                    """ % (row['Committee'], row['Name']))

        connection.commit()
        print("Added house committees for 115th session.")

    except pg.OperationalError as err:
        throw_psycopg2_exception(err)

def insert_house_committee_116():
    try:
        curs = connection.cursor()

        committees = pd.read_csv('..\webscraping\csv_data\\house_committee_membership_116.csv')
        for index, row in committees.iterrows():
            if row[1] not in (None, ""):
                if '"' in row['Committee']:
                    row['Committee'] = row['Committee'][1:-1]
                if row['Title'] == 'Chair':
                    curs.execute("""
                    INSERT INTO house_committee_116(hc_name, chair)
                    VALUES
                    (
                    '%s', '%s'
                    )
                    ON CONFLICT DO NOTHING
                    """ % (row['Committee'], row['Name']))

        connection.commit()
        print("Added house committees for 116th session.")

    except pg.OperationalError as err:
        throw_psycopg2_exception(err)

def insert_house_subcommittee_115():
    try:
        curs = connection.cursor()

        subcommittees = pd.read_csv('..\webscraping\csv_data\\house_committee_membership_115.csv')
        for index, row in subcommittees.iterrows():
            # print(row['Subcommittee'])
            if isinstance(row['Subcommittee'], str):
                if '"' in row['Subcommittee']:
                    row['Subcommittee'] = row['Subcommittee'][1:-1]
                if '"' in row['Committee']:
                    row['Committee'] = row['Committee'][1:-1]
                curs.execute("""
                INSERT INTO house_subcommittee_115(hsubc_name, sc_of)
                VALUES
                (
                '%s', '%s'
                )
                ON CONFLICT DO NOTHING
                """ % (row['Subcommittee'], row['Committee']))

        connection.commit()
        print("Subcommittee data for 115th session created.")

    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def insert_house_subcommittee_116():
    try:
        curs = connection.cursor()

        subcommittees = pd.read_csv('..\webscraping\csv_data\house_committee_membership_116.csv')
        for index, row in subcommittees.iterrows():
            # print(row['Subcommittee'])
            if isinstance(row['Subcommittee'], str):
                if '"' in row['Subcommittee']:
                    row['Subcommittee'] = row['Subcommittee'][1:-1]
                if '"' in row['Committee']:
                    row['Committee'] = row['Committee'][1:-1]
                curs.execute("""
                INSERT INTO house_subcommittee_116(hsubc_name, sc_of)
                VALUES
                (
                '%s', '%s'
                )
                ON CONFLICT DO NOTHING
                """ % (row['Subcommittee'], row['Committee']))

        connection.commit()
        print("Subcommittee data for 116th session created.")

    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def insert_house_com_rel_115():
    try:
        curs = connection.cursor()

        curs = connection.cursor()

        subcommittees = pd.read_csv('..\webscraping\csv_data\house_committee_membership_115.csv')
        for index, row in subcommittees.iterrows():
            # print(row['Subcommittee'])
            if isinstance(row['Subcommittee'], str):
                if '"' in row['Subcommittee']:
                    row['Subcommittee'] = row['Subcommittee'][1:-1]
                if '"' in row['Committee']:
                    row['Committee'] = row['Committee'][1:-1]
                curs.execute("""
                INSERT INTO house_com_rel_115(rep_name, hc_name, hsubc_name, title)
                VALUES
                (
                '%s', '%s', '%s', '%s'
                )
                ON CONFLICT DO NOTHING
                """ % (row['Name'], row['Committee'], row['Subcommittee'], row['Title']))

        connection.commit()
        print("Committee and subcommittee membership relational data for 115th session created.")

    except pg.OperationalError as err:
        throw_psycopg2_exception(err)

def insert_house_com_rel_116():
    try:
        curs = connection.cursor()

        curs = connection.cursor()

        subcommittees = pd.read_csv('..\webscraping\csv_data\house_committee_membership_116.csv')
        for index, row in subcommittees.iterrows():
            # print(row['Subcommittee'])
            if isinstance(row['Subcommittee'], str):
                if '"' in row['Subcommittee']:
                    row['Subcommittee'] = row['Subcommittee'][1:-1]
                if '"' in row['Committee']:
                    row['Committee'] = row['Committee'][1:-1]
                curs.execute("""
                INSERT INTO house_com_rel_116(rep_name, hc_name, hsubc_name, title)
                VALUES
                (
                '%s', '%s', '%s', '%s'
                )
                ON CONFLICT DO NOTHING
                """ % (row['Name'], row['Committee'], row['Subcommittee'], row['Title']))

        connection.commit()
        print("Committee and subcommittee membership relational data for 116th session created.")

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
        print("Loading Data from senators_115.csv")
        for index, row in reps.iterrows():
            print("Inserting row", row["Name"])
            curs.execute("""
            INSERT into senator_115(sen_name, state, party, terms, congress)
            VALUES (
                '%s', '%s', '%s', '%s', 115
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
'''
Functions to insert senate bills. These files were manually cleaned (they only required
single apostrophes to be replaced with double apostrophes.
'''

def insert_sen_bills_115():
    try:
        bills = pd.read_csv('..\webscraping\csv_data\senate_bills_115.csv')
        reps = pd.read_csv('..\webscraping\csv_data\senators_115.csv')

        rep_names = reps['Name'].tolist()

        curs = connection.cursor()
        print("Loading Data from senate_bills_115.csv")
        for index, row in bills.iterrows():
            if row['sponsors'] in rep_names:
                curs.execute("""
                INSERT into senate_bill_115(bill_name, description, bill_status, committees, sponsor, congress)
                VALUES
                (
                '%s', '%s', '%s', '%s', '%s', 115)
                """ % (row['names'].strip(), row['descriptions'].strip(), row['statuses'].strip(),
                       row['bill_committees'].strip(), row['sponsors'].strip())
                )
        connection.commit()
        print("Data from senate_bills_115.csv successfully inserted")

    except pg.OperationalError as err:
        throw_psycopg2_exception(err)

def insert_sen_bills_116():
    try:
        bills = pd.read_csv('..\webscraping\csv_data\senate_bills_116.csv')
        reps = pd.read_csv('..\webscraping\csv_data\senators_116.csv')

        rep_names = reps['Name'].tolist()

        curs = connection.cursor()
        print("Loading Data from senate_bills_116.csv")
        for index, row in bills.iterrows():
            if row['sponsors'] in rep_names:
                curs.execute("""
                INSERT into senate_bill_116(bill_name, description, bill_status, committees, sponsor, congress)
                VALUES
                (
                '%s', '%s', '%s', '%s', '%s', 116)
                """ % (row['names'].strip(), row['descriptions'].strip(), row['statuses'].strip(),
                       row['bill_committees'].strip(), row['sponsors'].strip())
                )
        connection.commit()
        print("Data from senate_bills_116.csv successfully inserted")

    except pg.OperationalError as err:
        throw_psycopg2_exception(err)

# --------------------------------------------------------------------------------------
'''
Insert senate committee/subcommittee data
'''

def insert_senate_committee_115():
    try:
        curs = connection.cursor()

        committees = pd.read_csv('..\webscraping\csv_data\\senate_committee_membership_115.csv')
        for index, row in committees.iterrows():
            if row[1] not in (None, ""):
                if '"' in row['Committee']:
                    row['sc_name'] = row['sc_name'][1:-1]
                if row['Title'] == 'Chairman':
                    curs.execute("""
                    INSERT INTO senate_committee_115(sc_name, chair)
                    VALUES
                    (
                    '%s', '%s'
                    )
                    ON CONFLICT DO NOTHING
                    """ % (row['Committee'], row['Name']))

        connection.commit()
        print("Added house committees and subcommittees for 115th session.")

    except pg.OperationalError as err:
        throw_psycopg2_exception(err)

def insert_senate_committee_116():
    try:
        curs = connection.cursor()

        committees = pd.read_csv('..\webscraping\csv_data\\senate_committee_membership_116.csv')
        for index, row in committees.iterrows():
            if row[1] not in (None, ""):
                if '"' in row['Committee']:
                    row['hc_name'] = row['hc_name'][1:-1]
                if row['Title'] == 'Chairman':
                    curs.execute("""
                    INSERT INTO senate_committee_116(sc_name, chair)
                    VALUES
                    (
                    '%s', '%s'
                    )
                    ON CONFLICT DO NOTHING
                    """ % (row['Committee'], row['Name']))

        connection.commit()
        print("Added house committees and subcommittees for 116th session.")

    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def insert_senate_subcommittee_115():
    try:
        curs = connection.cursor()

        subcommittees = pd.read_csv('..\webscraping\csv_data\\senate_committee_membership_115.csv')
        for index, row in subcommittees.iterrows():
            # print(row['Subcommittee'])
            if isinstance(row['Subcommittee'], str):
                if '"' in row['Subcommittee']:
                    row['Subcommittee'] = row['Subcommittee'][1:-1]
                if '"' in row['Committee']:
                    row['Committee'] = row['Committee'][1:-1]
                curs.execute("""
                INSERT INTO senate_subcommittee_115(ssubc_name, sc_of)
                VALUES
                (
                '%s', '%s'
                )
                ON CONFLICT DO NOTHING
                """ % (row['Subcommittee'], row['Committee']))

        connection.commit()
        print("Subcommittee data for 115th session created.")

    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def insert_senate_subcommittee_116():
    try:
        curs = connection.cursor()

        subcommittees = pd.read_csv('..\webscraping\csv_data\\senate_committee_membership_116.csv')
        for index, row in subcommittees.iterrows():
            # print(row['Subcommittee'])
            if isinstance(row['Subcommittee'], str):
                if '"' in row['Subcommittee']:
                    row['Subcommittee'] = row['Subcommittee'][1:-1]
                if '"' in row['Committee']:
                    row['Committee'] = row['Committee'][1:-1]
                curs.execute("""
                INSERT INTO senate_subcommittee_116(ssubc_name, sc_of)
                VALUES
                (
                '%s', '%s'
                )
                ON CONFLICT DO NOTHING
                """ % (row['Subcommittee'], row['Committee']))

        connection.commit()
        print("Subcommittee data for 116th session created.")

    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def insert_senate_com_rel_115():
    try:
        curs = connection.cursor()

        curs = connection.cursor()

        subcommittees = pd.read_csv('..\webscraping\csv_data\senate_committee_membership_115.csv')
        for index, row in subcommittees.iterrows():
            # print(row['Subcommittee'])
            if isinstance(row['Subcommittee'], str):
                if '"' in row['Subcommittee']:
                    row['Subcommittee'] = row['Subcommittee'][1:-1]
                if '"' in row['Committee']:
                    row['Committee'] = row['Committee'][1:-1]
                curs.execute("""
                INSERT INTO senate_com_rel_115(sen_name, sc_name, ssubc_name, title)
                VALUES
                (
                '%s', '%s', '%s', '%s'
                )
                ON CONFLICT DO NOTHING
                """ % (row['Name'], row['Committee'], row['Subcommittee'], row['Title']))

        connection.commit()
        print("Senate committee and subcommittee membership relational data for 115th session created.")

    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def insert_senate_com_rel_116():
    try:
        curs = connection.cursor()

        curs = connection.cursor()

        subcommittees = pd.read_csv('..\webscraping\csv_data\senate_committee_membership_116.csv')
        for index, row in subcommittees.iterrows():
            # print(row['Subcommittee'])
            if isinstance(row['Subcommittee'], str):
                if '"' in row['Subcommittee']:
                    row['Subcommittee'] = row['Subcommittee'][1:-1]
                if '"' in row['Committee']:
                    row['Committee'] = row['Committee'][1:-1]
                curs.execute("""
                INSERT INTO senate_com_rel_116(sen_name, sc_name, ssubc_name, title)
                VALUES
                (
                '%s', '%s', '%s', '%s'
                )
                ON CONFLICT DO NOTHING
                """ % (row['Name'], row['Committee'], row['Subcommittee'], row['Title']))
            if isinstance(row['Subcommittee'], float):
                if '"' in row ['Committee']:
                    row['Committee'] = row['Committee'][1:-1]
                curs.execute("""
                INSERT INTO senate_com_rel_116(sen_name, sc_name, title)
                VALUES
                (
                '%s', '%s', '%s'
                )
                ON CONFLICT DO NOTHING
                """ % (row['Name'], row['Committee'], row['Title']))

        connection.commit()
        print("Senate committee and subcommittee membership relational data for 116th session created.")

    except pg.OperationalError as err:
        throw_psycopg2_exception(err)

# --------------------------------------------------------------------------------------


# create_rep_table_115()                         # Created
# create_rep_table_116()                         # Created
# create_house_resolution_115()                  # Created
# create_house_resolution_116()                  # Created
# create_house_committee_table_115()             # Created
# create_house_committee_table_116()             # Created
# create_house_subcommittee_table_115()          # Created
# create_house_subcommittee_table_116()          # Created
# create_house_com_rel_table_115()               # Created
# create_house_com_rel_table_116()               # Created
# create_house_resolution_cosponsors_table_115() # Created
# create_house_resolution_cosponsors_table_116() # Created

# create_sen_table_115()                         # Created
# create_sen_table_116()                         # Created
# create_senate_bill_table_115()                 # Created
# create_senate_bill_table_116()                 # Created
# create_senate_committee_table_115()            # Created
# create_senate_committee_table_116()            # Created
# create_senate_subcommittee_table_115()         # Created
# create_senate_subcommittee_table_116()         # Created
# create_senate_com_rel_table_115()              # Created
create_senate_com_rel_table_116()              # Created
# create_sen_bill_cosponsors_table_115()         # Created
# create_sen_bill_cosponsors_table_116()         # Created

# fix_reps_115_csv()                             # DO NOT RUN
# fix_reps_116_csv()                             # DO NOT RUN
# insert_reps_115()                              # Executed
# insert_reps_116()                              # Executed
# insert_house_resolutions_115()                 # Executed
# insert_house_resolutions_116()                 # Executed
# insert_house_committee_115()                   # Executed
# insert_house_committee_116()                   # Executed
# insert_house_subcommittee_115()                # Executed
# insert_house_subcommittee_116()                # Executed
# insert_house_com_rel_115()                     # Executed
# insert_house_com_rel_116()                     # Executed

# insert_sen_115()                               # Executed
# insert_sen_116()                               # Executed
# insert_sen_bills_115()                         # Executed
# insert_sen_bills_116()                         # Executed
# insert_senate_committee_115()                  # Executed
# insert_senate_committee_116()                  # Executed
# insert_senate_subcommittee_115()               # Executed
# insert_senate_subcommittee_116()               # Executed
# insert_senate_com_rel_115()                    # Executed
insert_senate_com_rel_116()                    # Executed
