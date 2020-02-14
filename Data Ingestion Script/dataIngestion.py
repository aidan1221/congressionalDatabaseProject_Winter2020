import sys
import psycopg2 as pg
import csv
import pandas as pd

# --------------------------------- Make this read from a credentials csv?
DB_NAME = "REDACTED"
DB_USER = "REDACTED"
DB_PASSWORD = "REDACTED"
DB_HOST = "REDACTED"
DB_PORT = "REDACTED"
# ---------------------------------
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

