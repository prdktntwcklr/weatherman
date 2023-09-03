# simple script to convert a csv file into an sqlite database

import os
import pandas
import sqlite3
import sys


def main():
    # get the filename without extension
    filename = str(os.path.splitext(sys.argv[1])[0])

    # add appropriate extensions
    csvfile = filename + ".csv"
    dbfile = filename + ".db"

    try:
        dataframe = pandas.read_csv(csvfile)
    except FileNotFoundError:
        print(f"error: file {csvfile} not found")
        exit(1)

    conn = sqlite3.connect(dbfile)
    dataframe.to_sql(filename, conn, if_exists='replace', index=False)
    conn.close()


if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print(f"usage: python {os.path.basename(__file__)} <csv file>")
        exit(0)

    main()
