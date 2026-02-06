from cli import menu
import pytest


def test_choice_validation():
    invalid_choices = ["", "0", "4", "-1", "test", "     "]
    for choice in invalid_choices:
        with pytest.raises(ValueError):
            menu.validate_choice(choice)

    valid_choices = ["1", "2", "3", "exit"]
    for choice in valid_choices:
        assert menu.validate_choice(choice) == choice


# Test for UI level validation only
def test_url_validation():
    invalid_url = [
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
    ]
    for url in invalid_url:
        with pytest.raises(ValueError):
            menu.validate_url(url)

    valid_url = [
        "https://www.youtube.com/",
        "http://www.youtube.com/",
        "https://youtube.com/",
        "http://youtube.com/",
        "https://m.youtube.com/",
        "http://m.youtube.com/",
        "https://youtu.be/",
        "http://youtu.be/"
    ]

    for url in valid_url:
        assert menu.validate_url(url) == url

    assert menu.validate_url("exit") == "exit"
