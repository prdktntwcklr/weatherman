"""
simple script to convert a csv file into an sqlite database named 'database'
"""

import os
import pandas
import sqlite3
import sys

from pathlib import Path


def convert_csv_to_sqlite(csvfile: Path, dbfile: Path) -> None:
    """
    Converts a CSV file into a SQLite database.

    This function reads the contents of a CSV file into a pandas DataFrame
    and writes it to a new or existing SQLite database file using a fixed
    table name `"database"`. If the table already exists, it is replaced.

    Args:
        csvfile (Path): Path to the input CSV file to be converted.
        dbfile (Path): Path to the output SQLite database file to create or
        overwrite.
    """
    if not os.path.exists(csvfile):
        raise FileNotFoundError("CSV File not found")

    try:
        dataframe = pandas.read_csv(csvfile)
        conn = sqlite3.connect(dbfile)
        # Use a fixed table name ("database") — required by the backend for
        # lookups.
        dataframe.to_sql("database", conn, if_exists="replace", index=False)
    finally:
        conn.close()


def get_filename_without_extensions(path: str) -> str:
    """
    Removes all file extensions from a given path.

    Example:
        >>> get_filename_without_all_extensions("archive.tar.gz")
        'archive'
        >>> get_filename_without_all_extensions("/tmp/data.backup.zip")
        '/tmp/data'
    """
    root = path
    while True:
        root, ext = os.path.splitext(root)
        if not ext:
            break
    return root


def main():
    if len(sys.argv) != 2:
        print(f"usage: python {os.path.basename(__file__)} <csv file>")
        exit(1)

    csv_file = sys.argv[1]
    filename = get_filename_without_extensions(csv_file)

    csvfile = filename + ".csv"
    dbfile = filename + ".db"

    convert_csv_to_sqlite(csvfile, dbfile)


if __name__ == "__main__":
    main()
