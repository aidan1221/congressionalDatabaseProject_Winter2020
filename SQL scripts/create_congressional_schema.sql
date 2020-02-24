DROP DATABASE if exists congressionalscrapings;
CREATE DATABASE congressionalscrapings owner postgres;
\connect congressionalscrapings

DROP TABLE if exists representative;
CREATE TABLE representative (
    rep_name varchar(255) UNIQUE NOT NULL,
    state varchar(255),
    district integer,
    party varchar(255),
    terms varchar(255),
    congress int,
    PRIMARY KEY (rep_name, state)
);

ALTER TABLE representative OWNER to postgres;

DROP TABLE if exists house_resolution;
CREATE TABLE house_resolution (
    res_name varchar(255) PRIMARY KEY NOT NULL,
    sponsor varchar(255) REFERENCES representative(rep_name),
    committees varchar(255),
    status varchar(255),
    description varchar(500)
);

ALTER TABLE house_resolution OWNER to postgres;

DROP TABLE if exists house_committee;
CREATE TABLE house_committee (
    hc_name varchar(255)NOT NULL,
    chair varchar(255) NOT NULL REFERENCES representative(rep_name),
    ranking_member varchar(255) REFERENCES representative(rep_name),
    PRIMARY KEY (hc_name, chair)
);

ALTER TABLE house_committee OWNER to postgres;

DROP TABLE if exists house_subcommittee;
CREATE TABLE house_subcommittee (
    hsubc_name varchar(255) NOT NULL,
    sc_of varchar(255) REFERENCES house_committee(hc_name),
    PRIMARY KEY (hsubc_name, sc_of)
);

ALTER TABLE house_subcommittee OWNER to postgres;

DROP TABLE if exists house_com_rel;
CREATE TABLE house_com_rel (
  rep_name varchar(255) REFERENCES representative(rep_name),
  hc_name varchar(255) REFERENCES house_committee(hc_name),
  chair varchar(3),
  ranking_member varchar(3),
  CONSTRAINT CHK_CHAIR CHECK (chair in ('yes', 'no')),
  CONSTRAINT CHK_RNK_MEM CHECK (ranking_member in ('yes', 'no'))
);

ALTER TABLE house_com_rel OWNER to postgres;

DROP TABLE if exists res_cosponsors;
CREATE TABLE res_cosponsors (
  res_name varchar(255) NOT NULL REFERENCES house_resolution(res_name),
  cosponsor varchar(255) NOT NULL REFERENCES representative(rep_name),
  PRIMARY KEY (res_name, cosponsor)
);

ALTER TABLE res_cosponsors OWNER to postgres;

DROP TABLE if exists senator;
CREATE TABLE senator (
  sen_name varchar(255) UNIQUE NOT NULL,
  state varchar (255),
  party varchar(255),
  terms varchar(255),
  congress int,
  PRIMARY KEY (senator, state)
);

ALTER TABLE senator OWNER to postgres;

DROP TABLE if exists senate_bill;
CREATE TABLE senate_bill(
   bill_name varchar(255) PRIMARY KEY NOT NULL,
   sponsor varchar(255) REFERENCES senator(sen_name),
   committees varchar(255),
   bill_status varchar(255),
   description varchar(500)
);

ALTER TABLE senate_bill OWNER to postgres;

DROP TABLE if exists senate_committee;
CREATE TABLE senate_committee (
    sc_name varchar(255) UNIQUE NOT NULL,
    chair varchar(255) NOT NULL REFERENCES senator(sen_name),
    ranking_member varchar(255) REFERENCES senator(sen_name),
    PRIMARY KEY (sc_name, chair)
);

ALTER TABLE senate_committee OWNER to postgres;

DROP TABLE if exists senate_subcommittee;
CREATE TABLE senate_subcommittee (
    ssubc_name varchar(255) NOT NULL,
    sc_of varchar(255) REFERENCES senate_committee(sc_name),
    PRIMARY KEY (ssubc_name, sc_of)
);

ALTER TABLE senate_committee OWNER to postgres;

DROP TABLE if exists senate_com_rel;
CREATE TABLE senate_com_rel (
  sen_name varchar(255) REFERENCES senator(sen_name),
  sc_name varchar(255) REFERENCES senate_committee(sc_name),
  chair varchar(3),
  ranking_member varchar(3),
  CONSTRAINT CHK_CHAIR CHECK (chair in('yes', 'no')),
  CONSTRAINT CHK_RNK_MEM CHECK (ranking_member in ('yes', 'no'))
);

ALTER TABLE senate_com_rel OWNER to postgres;

DROP TABLE if exists bill_cosponsors;
CREATE TABLE bill_cosponsors (
  bill_name varchar(255) NOT NULL REFERENCES senate_bill(bill_name),
  cosponsor varchar(255) NOT NULL REFERENCES senator(sen_name),
  PRIMARY KEY (bill_name, cosponsor)
);

ALTER TABLE bill_cosponsors OWNER to postgres;
