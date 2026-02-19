from helpers import system_check
from unittest.mock import patch

def test_dependency_checking():
    with patch("shutil.which", return_value = None):
        assert system_check.check_dependency() == False