import os
import pytest
from utils import read_file, write_file, append_file

# Use pytest tmp_path fixture for temp files
def test_write_and_read_file(tmp_path):
    test_file = tmp_path / "testfile.txt"
    
    # Write lines
    lines = ["line1", "line2"]
    write_file(test_file, lines)
    
    # Read lines
    result = read_file(test_file)
    assert result == lines

def test_append_file(tmp_path):
    test_file = tmp_path / "testfile.txt"
    
    # Write initial lines
    write_file(test_file, ["line1"])
    
    # Append a line
    append_file(test_file, "line2")
    
    # Read all lines
    result = read_file(test_file)
    assert result == ["line1", "line2"]

import pytest
from test_smartmart import cashier_exists, write_file, CASHIERS_FILE

def test_cashier_exists(tmp_path):
    # Create a temporary file for cashiers
    test_file = tmp_path / "cashiers.txt"
    write_file(test_file, ["john:1234", "jane:abcd"])

    # Patch CASHIERS_FILE global variable to point to the temp file
    global CASHIERS_FILE
    CASHIERS_FILE = str(test_file)

    assert cashier_exists("john") is True
    assert cashier_exists("mike") is False


