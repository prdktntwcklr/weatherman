import pytest
import sqlite3
import sys

from pathlib import Path
from csv_converter import convert_csv_to_sqlite, get_filename_without_extensions


def create_sample_csv(tmp_path: Path) -> Path:
    """
    Helper that creates a temporary CSV file with sample data
    and returns its path.
    """
    csv_file = tmp_path / "orders.csv"
    csv_content = (
        "OrderID,CustomerName,Amount,IsActive,TransactionDate\n"
        "101,Alice Smith,45.50,True,2023-10-01\n"
        "102,\"Bob, J.\",120.00,False,2023-10-02\n"
        "103,Charlie,5.99,True,2023-10-03\n"
    )
    csv_file.write_text(csv_content)
    return csv_file

def create_header_only_csv(tmp_path: Path) -> Path:
    """
    Helper that creates a temporary CSV file that only includes a header and no
    data.
    """
    csv_file = tmp_path / "header_only.csv"
    csv_content = (
        "ID,Name,Value\n"
    )
    csv_file.write_text(csv_content)
    return csv_file


def test_non_existing_file_should_throw_error(tmp_path: Path):
    """Ensure that missing input CSV raises a FileNotFoundError and doesn't create a DB file."""
    non_existent_csv = tmp_path / "non_existent.csv"
    db_file = tmp_path / "out.db"

    with pytest.raises(FileNotFoundError):
        convert_csv_to_sqlite(non_existent_csv, db_file)

    assert not db_file.exists(), "Database file must not be created if CSV is missing."


def test_successful_conversion(tmp_path: Path):
    """Verify that conversion produces the correct table structure and data."""
    csv_file = create_sample_csv(tmp_path)
    db_file = tmp_path / "orders.db"
    table_name = "database"

    convert_csv_to_sqlite(csv_file, db_file)
    assert db_file.exists(), "SQLite database should be created after conversion."

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        # Check table existence
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,)
        )
        assert cursor.fetchone(), f"Table '{table_name}' should exist in the database."

        # Check column names
        expected_columns = [
            "OrderID", "CustomerName", "Amount", "IsActive", "TransactionDate"
        ]
        cursor.execute(f"PRAGMA table_info({table_name})")
        actual_columns = [col[1] for col in cursor.fetchall()]
        assert actual_columns == expected_columns, f"Column mismatch: {actual_columns} != {expected_columns}"

        # Check row data
        cursor.execute(f"SELECT * FROM {table_name} ORDER BY OrderID")
        results = cursor.fetchall()
        expected_data = [
            (101, "Alice Smith", 45.50, 1, "2023-10-01"),
            (102, "Bob, J.", 120.00, 0, "2023-10-02"),
            (103, "Charlie", 5.99, 1, "2023-10-03"),
        ]
        assert results == expected_data, "Inserted rows do not match expected content."
    finally:
        conn.close()


def test_empty_csv_creates_empty_table(tmp_path: Path):
    """Ensure that a CSV with only a header creates an empty table with correct columns."""
    csv_file = create_header_only_csv(tmp_path)
    db_file = tmp_path / "empty.db"
    table_name = "database"

    convert_csv_to_sqlite(csv_file, db_file)
    assert db_file.exists(), "Database should be created even for header-only CSV."

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        # Table should exist
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,)
        )
        assert cursor.fetchone(), "Table should exist even with no data rows."

        # Column count should match header count
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        assert len(columns) == 3, f"Expected 3 columns, got {len(columns)}."

        # Table should be empty
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        assert count == 0, "Table should have 0 rows when CSV has no data."
    finally:
        conn.close()


@pytest.mark.parametrize(
    "input_path,expected",
    [
        ("file.txt", "file"),
        ("/tmp/example.csv", "/tmp/example"),
        ("./nested/data.json", "./nested/data"),
        ("report", "report"),  # no extension
        ("archive.tar.gz", "archive"),  # removes all extensions
        ("C:\\path\\to\\windows_file.txt", "C:\\path\\to\\windows_file"),  # Windows paths
    ],
)
def test_get_filename_without_extensions(input_path, expected):
    """Ensure the filename is correctly stripped of all extensions."""
    result = get_filename_without_extensions(input_path)
    assert result == expected

