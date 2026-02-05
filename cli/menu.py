from colorama import Fore
import sys
import time

MAIN_PROMPT = """

Welcome to EZ Youtube Downloader!

To get started, choose among the options below:

1. Single Download
2. Batch Download
3. Playlist Download


Note: You can type "exit" anytime to close the program :)

"""

TYPE_PROMPT = """
What format do you want to download?

1. Video
2. Audio only

"""

URL_PROMPT = """
Please enter Youtube URL (copy-paste it below)

"""

DELAY = 1.5


def exit_program() -> None:
    print(Fore.GREEN + "\nThank you for using EZ Youtube Downloader!")
    sys.exit()


def get_user_choice() -> str:
    while True:
        try:
            return validate_choice(input(Fore.WHITE + MAIN_PROMPT).strip().lower())
        except ValueError:
            print(Fore.RED + '\nInvalid input. Please enter from value 1-3 or "exit"')
            time.sleep(DELAY)
            continue


def validate_choice(choice: str) -> str:
    if choice != "exit" and int(choice) not in range(1,4):
        raise ValueError
    return choice


def get_type() -> str:
    while True:
        try:
            return validate_type(input(Fore.WHITE + TYPE_PROMPT).strip().lower())
        except ValueError:
            print(Fore.RED + "\nInvalid input. Please enter 1, 2, or exit")
            time.sleep(DELAY)


def validate_type(type: str) -> str:
    if type != "exit" and int(type) not in range(1,3):
        raise ValueError
    return type


def get_url() -> str:
    while True:
        try:
            return validate_url(input(Fore.WHITE + URL_PROMPT)).strip()
        except ValueError:
            #Edit exception here
            print(Fore.RED + "\nInvalid URL. Please copy-paste Youtube URL")


def validate_url(url: str) -> str:
    if url.lower() != "exit" and url == "":
        raise ValueError
    return url
