from cli import menu
from pathlib import Path
import pytest


# Validates user choice in main menu
def test_choice_validation():
    invalid_choices = ("", "0", "4", "-1", "test", "     ")
    for choice in invalid_choices:
        with pytest.raises(ValueError):
            menu.validate_choice(choice)

    valid_choices = ("1", "2", "exit")
    for choice in valid_choices:
        assert menu.validate_choice(choice) == choice


# Validates user input for URL. (UI level validation only)
def test_url_validation():
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


# Validates user input in type of file
def test_type_validation():
    invalid_types = ("0", "3", "", "    ", "test", "123", "-1", "---")

    for _type in invalid_types:
        with pytest.raises(ValueError):
            menu.validate_type(_type)

    assert menu.validate_type("exit") == "exit"
    assert menu.validate_type("1") == "video"
    assert menu.validate_type("2") == "audio"


# Validates user's input for filepath on where to save the downloaded files
def test_filepath_validation(tmp_path):
    invalid_filepaths = ("test", "123", "---", "1:/test", "-:/test")

    for filepath in invalid_filepaths:
        with pytest.raises(ValueError):
            menu.validate_filepath(filepath)

    assert menu.validate_filepath("") == Path(__file__).parent.parent
    assert menu.validate_filepath("no") == Path(__file__).parent.parent

    temp_dir = tmp_path / "my_temp_dir"
    temp_dir.mkdir()

    assert menu.validate_filepath(str(temp_dir)) == temp_dir

    temp_file = tmp_path / "temp_file.txt"
    temp_file.touch()

    with pytest.raises(NotADirectoryError):
        menu.validate_filepath(str(temp_file))


# Validates the user input for yes or no decisions
def test_decision_validation():
    invalid_decisions = ("", "      ", "test", "123", "---", "-a1")

    for decision in invalid_decisions:
        with pytest.raises(ValueError):
            menu.validate_decision(decision)

    valid_decisions = ("y", "n", "exit")

    for decision in valid_decisions:
        assert menu.validate_decision(decision) == decision


# Validates user input for filepath of their txt file for batch downloading
def test_url_list_file_validation(tmp_path):
    assert menu.validate_url_list_file("exit") == "exit"

    invalid_filenames = [
        "",
        "filename",
        "filename.csv",
        ".filename.txt",
        ".filename..txt",
    ]

    for filename in invalid_filenames:
        with pytest.raises(ValueError):
            menu.validate_url_list_file(filename)

    with pytest.raises(FileNotFoundError):
        menu.validate_url_list_file("missing_file.txt")

    temp_dir = tmp_path / "my_temp_dir.txt"
    temp_dir.mkdir()

    with pytest.raises(IsADirectoryError):
        menu.validate_url_list_file(str(temp_dir))
