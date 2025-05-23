
from main import cashier_exists, write_file

def test_cashier_exists(tmp_path):
    test_file = tmp_path / "cashiers.txt"
    write_file(test_file, ["john:1234", "jane:abcd"])
    
    assert cashier_exists("john", filename=str(test_file)) is True
    assert cashier_exists("mike", filename=str(test_file)) is False

from main import write_file, is_valid_login

def test_valid_login(tmp_path):
    test_file = tmp_path / "admin.txt"
    write_file(test_file, ["admin:adminpass"])

    assert is_valid_login("admin", "adminpass", filename=str(test_file)) is True
    assert is_valid_login("admin", "wrongpass", filename=str(test_file)) is False
