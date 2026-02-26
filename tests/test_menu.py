from cli import menu
from unittest.mock import patch
import pytest


def test_choice_validation():
    """Validates user choice in main menu"""
    invalid_choices = ("", "0", "4", "-1", "test", "     ")
    for choice in invalid_choices:
        with pytest.raises(ValueError):
            menu.validate_choice(choice)

    valid_choices = ("1", "2", "exit")
    for choice in valid_choices:
        assert menu.validate_choice(choice) == choice


def test_url_validation():
    """Validates user input for URL. (UI level validation only)"""
    invalid_url = (
        "",
        "     ",
        "test",
        "12345",
        "----",
        "12test34-",
        "www.facebook.com/",
        "https://.youtube.com/",
        "https://you.tube.com/",
        "https://youtube.com./",
    )
    for url in invalid_url:
        with pytest.raises(ValueError):
            menu.validate_url(url)

    valid_url = (
        "https://www.youtube.com/",
        "http://www.youtube.com/",
        "https://youtube.com/",
        "http://youtube.com/",
        "https://m.youtube.com/",
        "http://m.youtube.com/",
        "https://youtu.be/",
        "http://youtu.be/",
    )

    for url in valid_url:
        assert menu.validate_url(url) == url

    assert menu.validate_url("exit") == "exit"
    assert menu.validate_url("cancel") == "cancel"


def test_type_validation():
    """Validates user input in type of file"""
    invalid_types = ("0", "3", "", "    ", "test", "123", "-1", "---")

    for _type in invalid_types:
        with pytest.raises(ValueError):
            menu.validate_type(_type)

    assert menu.validate_type("exit") == "exit"
    assert menu.validate_type("cancel") == "cancel"
    assert menu.validate_type("1") == "video"
    assert menu.validate_type("2") == "audio"


def test_decision_validation():
    """Validates the user input for yes or no decisions"""
    invalid_decisions = ("", "      ", "test", "123", "---", "-a1")

    for decision in invalid_decisions:
        with pytest.raises(ValueError):
            menu.validate_decision(decision)

    valid_decisions = ("y", "n", "exit", "cancel")

    for decision in valid_decisions:
        assert menu.validate_decision(decision) == decision


def test_url_list_file_validation(tmp_path):
    """Validates user input for getting url list file depending on users action based on given steps"""
    assert menu.validate_url_list_file_input("exit") == "exit"
    assert menu.validate_url_list_file_input("cancel") == "cancel"

    fake_home = tmp_path
    fake_desktop = tmp_path / "Desktop"
    fake_desktop.mkdir()

    with patch("pathlib.Path.home", return_value=fake_home):
        with pytest.raises(FileNotFoundError):
            menu.validate_url_list_file_input("proceed")

        fake_file = fake_desktop / "ez.txt"
        fake_file.mkdir()

        with pytest.raises(IsADirectoryError):
            menu.validate_url_list_file_input("proceed")
        fake_file.rmdir()

        fake_file.touch()

        test_errors = [PermissionError, OSError]
        for error in test_errors:
            with patch("pathlib.Path.open", side_effect=error):
                with pytest.raises(error):
                    menu.validate_url_list_file_input("proceed")

        assert menu.validate_url_list_file_input("proceed") == fake_file
