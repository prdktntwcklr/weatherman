import pytest
import sqlite3

from csv_converter import convert_csv_to_sqlite

def test_non_existing_file_should_throw_error(tmp_path):
    tmp_db_file = tmp_path / "tmp_file.db"

    with pytest.raises(Exception) as e:
        convert_csv_to_sqlite("non_existing_file.csv", tmp_db_file)

def test_successfull_conversion(tmp_path):
    tmp_csv_file = tmp_path / "orders.csv"
    csv_content = (
        "OrderID,CustomerName,Amount,IsActive,TransactionDate\n"
        "101,Alice Smith,45.50,True,2023-10-01\n"
        "102,\"Bob, J.\",120.00,False,2023-10-02\n"
        "103,Charlie,5.99,True,2023-10-03\n"
    )
    tmp_csv_file.write_text(csv_content)

    tmp_db_file = tmp_path / "orders.db"

    # table name is hardcoded as "database"
    table_name = "database"

    convert_csv_to_sqlite(tmp_csv_file, tmp_db_file)

    assert tmp_db_file.is_file(), "The SQLite database file was not created."
    
    conn = sqlite3.connect(tmp_db_file)
    cursor = conn.cursor()

    try:
        # assert the table exists
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        assert cursor.fetchone() is not None, f"Table '{table_name}' was not found."

        # assert the column names and count are correct
        expected_column_names = [
            'OrderID', 
            'CustomerName',
            'Amount', 
            'IsActive', 
            'TransactionDate'
        ]

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        assert len(columns) == len(expected_column_names), \
            f"Expected {len(expected_column_names)} columns but found {len(columns)}."

        actual_column_names = [col_info[1] for col_info in columns]

        assert actual_column_names == expected_column_names, \
            f"Column names do not match. Found: {actual_column_names}"

        # assert actual data is correct
        cursor.execute(f"SELECT * FROM {table_name} ORDER BY OrderID")
        results = cursor.fetchall()

        assert len(results) == 3, "Incorrect number of rows inserted."

        expected_data = [
            (101, 'Alice Smith', 45.50, 1, '2023-10-01'),
            (102, 'Bob, J.', 120.00, 0, '2023-10-02'),
            (103, 'Charlie', 5.99, 1, '2023-10-03')
        ]

        assert results == expected_data, "The inserted data does not match the expected CSV content."   

    finally:
        conn.close()