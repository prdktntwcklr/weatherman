# simple script to convert a csv file into an sqlite database named 'database'

import os
import pandas
import sqlite3
import sys

from pathlib import Path

def convert_csv_to_sqlite(csvfile: Path, dbfile: Path) -> None:
    if not os.path.exists(csvfile):
        raise FileNotFoundError("CSV File not found")

    try:
        dataframe = pandas.read_csv(csvfile)
        conn = sqlite3.connect(dbfile)
        # Use a fixed table name ("database") — required by the backend for data lookups.
        dataframe.to_sql("database", conn, if_exists='replace', index=False)
    finally:
        conn.close()


def get_filename_without_extension():
    """Extracts the filename (without extension) from the first CLI argument."""
    return str(os.path.splitext(sys.argv[1])[0])


def main():
    # get the filename without extension
    filename = get_filename_without_extension()

    csvfile = filename + ".csv"
    dbfile = filename + ".db"

    convert_csv_to_sqlite(csvfile, dbfile)


if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print(f"usage: python {os.path.basename(__file__)} <csv file>")
        exit(0)

    main()
