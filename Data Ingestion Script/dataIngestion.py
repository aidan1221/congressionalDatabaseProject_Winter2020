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


def create_rep_table():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE representative (
                rep_name varchar(255) UNIQUE NOT NULL,
                state varchar(255),
                district integer,
                party varchar(255),
                address varchar(255),
                PRIMARY KEY (rep_name, state)
                );
        """)
        curs.execute("""
                ALTER TABLE representative OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - Representative table created.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_house_resolution():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE house_resolution (
                res_name varchar(255) PRIMARY KEY NOT NULL,
                sponsor varchar(255) REFERENCES representative(rep_name),
                committees varchar(255),
                status varchar(255),
                description varchar(1000)
                );
        """)
        curs.execute("""
                ALTER TABLE house_resolution OWNER to postgres
        """)
        connection.commit()
        print("Operation Succeeded - House Resolution table created.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_house_committee_table():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE house_committee (
                hc_name varchar(255) UNIQUE NOT NULL,
                chair varchar(255) NOT NULL REFERENCES representative(rep_name),
                ranking_member varchar(255) REFERENCES representative(rep_name),
                PRIMARY KEY (hc_name, chair)
                );
        """)
        curs.execute("""
                ALTER TABLE house_committee OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - House Committee table created.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_house_subcommittee_table():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE house_subcommittee (
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
                CREATE TABLE house_com_rel (
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
                CREATE TABLE res_cosponsors (
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


def create_sen_table():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE senator (
                sen_name varchar(255) UNIQUE PRIMARY KEY NOT NULL,
                state varchar (255),
                party varchar(255),
                address varchar(255)
                );
        """)
        curs.execute("""
                ALTER TABLE senator OWNER to postgres;
        """)
        connection.commit()
        print("Operation Succeeded - Senator table created.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)


def create_senate_bill_table():
    curs = connection.cursor()

    try:
        curs.execute("""
                CREATE TABLE senate_bill(
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
                CREATE TABLE senate_committee (
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
                CREATE TABLE senate_subcommittee (
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
                CREATE TABLE senate_com_rel (
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
                CREATE TABLE bill_cosponsors (
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

def insert_reps():
    try:
        reps = pd.read_csv('representative.csv')
        curs = connection.cursor()
        print("Loading Data from representative.csv")
        for index, row in reps.iterrows():
            curs.execute("""
            INSERT into congressionalscrapings.representative(rep_name, state, district, party, address)
            VALUES (
                '%s', '%s', %d, '%s', '%s'
            )"""(row['rep_name'].strip(), row['state'].strip(), int(row['district']), row['party'].strip(), row['address'].strip())
            )

        connection.commit()
        print("Data from Representative.csv successfully inserted.")
    except pg.OperationalError as err:
        throw_psycopg2_exception(err)

def insert_house_bills():
    try:
        bills = pd.read_csv('house_bills.csv')
        reps = pd.read_csv('representative.csv')

        rep_names = reps['rep_name'].tolist()

        curs = connection.cursor()
        print("Loading Data from house_bills.csv")
        for index, row in bills.iterrows():
            if row['sponsor'] in rep_names:
                curs.execute("""
                INSERT into congressionalscrapings.representative(res_name, sponsor, committees, status, description)
                VALUES
                (
                '%s', '%s', '%s', '%s', '%s')
                """ % (row['hrname'].strip(), row['sponsor'].strip(), row['committees'].strip()), row['status'].strip(), row['description'].strip())
        connection.commit()
        print("Data from House Bills successfully inserted")
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

create_rep_table()
create_house_committee_table()
create_house_subcommittee_table()
create_house_committee_relational_table()
create_house_resolution()

create_sen_table()
create_senate_committee_table()
create_senate_subcommittee_table()
create_senate_com_rel_table()
create_senate_bill_table()
create_sen_bill_cosponsors_table()

insert_reps()
insert_house_bills()
insert_house_committee()
