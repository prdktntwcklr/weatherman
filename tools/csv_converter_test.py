import pytest

from csv_converter import convert_csv_to_sqlite

def test_non_existing_file_should_throw_error():
    with pytest.raises(Exception) as e:
        convert_csv_to_sqlite("non_existing_file.csv", "output.db")

def test_existing_file_should_pass(tmp_path):
    # create a temporary file with some content
    temp_file = tmp_path / "temp_file.csv"
    csv_content = "header1,header2\nvalue1,value2\n" 
    temp_file.write_text(csv_content)

    convert_csv_to_sqlite(temp_file, "output.db")
