# CSV to SQLite converter

A simple Python script to convert a CSV file into an SQLite database.

Basic usage:

```bash
python csv-to-sqlite.py <mydata.csv>
```

This will create an SQLite file named mydata.db in the same directory as the CSV
file.

## SQLite Viewer

To confirm that the SQLite file has been successfully created, you can use a
handy online tool called [SQLite Viewer](https://inloop.github.io/sqlite-viewer/)
to display its contents.

## Sample Data

The `examples` folder contains temperature and humidity data that shows a sample
output file obtained from running the script.