import pytest
import sqlite3

from csv_converter import convert_csv_to_sqlite
from pathlib import Path


@pytest.fixture
def converted_db_connection(tmp_path: Path):
    """
    Fixture that creates a CSV file, runs the conversion, and yields a 
    live sqlite3 connection for assertions. Closes the connection on teardown.
    """
    tmp_csv_file = tmp_path / "orders.csv"
    tmp_db_file = tmp_path / "orders.db"
    table_name = "database"

    csv_content = (
        "OrderID,CustomerName,Amount,IsActive,TransactionDate\n"
        "101,Alice Smith,45.50,True,2023-10-01\n"
        "102,\"Bob, J.\",120.00,False,2023-10-02\n"
        "103,Charlie,5.99,True,2023-10-03\n"
    )
    tmp_csv_file.write_text(csv_content)

    convert_csv_to_sqlite(tmp_csv_file, tmp_db_file)
    
    assert tmp_db_file.is_file(), "Fixture failed: The SQLite database file was not created by convert_csv_to_sqlite."

    conn = sqlite3.connect(tmp_db_file)
    yield conn, table_name

    conn.close()


def test_non_existing_file_should_throw_error(tmp_path: Path):
    tmp_db_file = tmp_path / "tmp_file.db"

    with pytest.raises(Exception) as e:
        convert_csv_to_sqlite("non_existing_file.csv", tmp_db_file)


def test_successfull_conversion(converted_db_connection):
    """
    Test that uses the fixture to assert table existence, column structure, 
    and data content.
    """
    conn, table_name = converted_db_connection
    cursor = conn.cursor()

    expected_column_names = [
        'OrderID', 
        'CustomerName',
        'Amount', 
        'IsActive', 
        'TransactionDate'
    ]
    expected_data = [
        (101, 'Alice Smith', 45.50, 1, '2023-10-01'),
        (102, 'Bob, J.', 120.00, 0, '2023-10-02'),
        (103, 'Charlie', 5.99, 1, '2023-10-03')
    ]
    
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    assert cursor.fetchone() is not None, f"Table '{table_name}' was not found in the database."

    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    assert len(columns) == len(expected_column_names), "Incorrect number of columns."
    actual_column_names = [col_info[1] for col_info in columns]
    assert actual_column_names == expected_column_names, "Column names do not match."

    # Note: Using ORDER BY is crucial for reliable testing
    cursor.execute(f"SELECT * FROM {table_name} ORDER BY OrderID")
    results = cursor.fetchall()

    assert len(results) == len(expected_data), "Incorrect number of rows inserted."
    assert results == expected_data, "The inserted data does not match the expected content."
