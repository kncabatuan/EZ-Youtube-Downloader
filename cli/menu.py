from cli import prompts
from colorama import Fore
from helpers import downloader
from pathlib import Path
import re
import sys
import time

# Time used for delay using time.sleep (in seconds)
DELAY = 1.5


def get_user_choice() -> str:
    """
    Gets user input for Main Menu and calls validator function

    Returns:
        str: The validated user input
    """
    while True:
        print(Fore.YELLOW + prompts.MAIN_PROMPT_1)
        try:
            return validate_choice(
                input(Fore.WHITE + prompts.MAIN_PROMPT_2).strip().lower()
            )
        except ValueError:
            print(Fore.RED + '\nInvalid input. Please enter from value 1-3 or "exit"')
            time.sleep(DELAY)


def validate_choice(choice: str) -> str:
    """
    Validates user input from caller

    Args:
        choice (str): The user input

    Returns:
        str: The validated choice ("1", "2", "3", or "exit")

    Raises:
        ValueError: If choice is not "1", "2", "3", or "exit"
    """
    if choice != "exit" and int(choice) not in range(1, 4):
        raise ValueError
    return choice


def get_url() -> str:
    """
    Gets user input for URL and calls validator function

    Returns:
        str: The validated URL
    """
    while True:
        print(Fore.YELLOW + prompts.URL_PROMPT)
        try:
            return validate_url(input(Fore.WHITE + "")).strip()
        except ValueError:
            print(Fore.RED + "\nInvalid URL. Please copy-paste Youtube URL")
            time.sleep(DELAY)


def validate_url(url: str) -> str:
    """
    Validates user input from caller

    Args:
        url (str): The user's URL input

    Returns:
        str: The validated URL or "exit"

    Raises:
        ValueError: If input is empty, regex is not recognized in input, or input is not exit
    """
    pattern = r"^(?:https?://)?(?:www\.|m\.)?(?:youtube\.com|youtu\.be)/"
    if url.lower() != "exit" and not re.search(pattern, url):
        raise ValueError

    if url == "":
        raise ValueError

    return url


def get_type() -> str:
    """
    Gets user input for File Type and calls validator function

    Returns:
        str: The file type ("video"/"audio") or "exit"
    """
    while True:
        print(Fore.YELLOW + prompts.TYPE_PROMPT_1)
        try:
            return validate_type(
                input(Fore.WHITE + prompts.TYPE_PROMPT_2).strip().lower()
            )
        except ValueError:
            print(Fore.RED + "\nInvalid input. Please enter 1, 2, or exit")
            time.sleep(DELAY)


def validate_type(file_type: str) -> str:
    """
    Validates user input from caller

    Args:
        file_type (str): The user's file_type input

    Returns:
        str: The validated file_type ("video" or "audio") or "exit"

    Raises:
        ValueError: If input is not "1", "2", or "exit"
    """
    if file_type != "exit" and int(file_type) not in range(1, 3):
        raise ValueError

    if file_type == "exit":
        return file_type
    if int(file_type) == 1:
        return "video"
    if int(file_type) == 2:
        return "audio"

    raise ValueError


def get_filepath() -> str | Path:
    """
    Prompts user for file path to save the downloaded file, if any

    Loops until a valid path is obtained

    Returns:
        Path: The validated file path (object)
        str: "exit" if the user wants to close the program
    """
    while True:
        print(Fore.YELLOW + prompts.PATH_PROMPT_1)
        try:
            return validate_filepath(input(Fore.WHITE + prompts.PATH_PROMPT_2).strip())
        except ValueError:
            print(
                Fore.RED + "\nInvalid filepath. Please follow correct format",
                Fore.RED + "\nC:\\... or C:/...",
            )
            time.sleep(DELAY)
        except NotADirectoryError:
            print(
                Fore.RED
                + "\nFilepath provided is not a directory. Please enter a valid one",
            )
            time.sleep(DELAY)
        except PermissionError:
            print(
                Fore.RED + "\nYou don't have enough permission to access this folder.",
            )
            time.sleep(DELAY)
        except OSError:
            print(
                Fore.RED + "\nSomething went wrong when accessing the folder",
            )
            time.sleep(DELAY)


def validate_filepath(filepath: str) -> str | Path:
    """
    Validates user input for file path

    Args:
        filepath (str): The user input for file path

    Returns:
        Path: The validated file path (object)
        str: "exit" if the user wants to close the program

    Raises:
        ValueError: If the user input is invalid
        NotADirectoryError: If the path is not a directory
        PermissionError: If the user does not have permission to access the directory
        OSError: If other OS-related error occurred
    """
    if filepath == "exit":
        return filepath

    valid_path = downloader.Save_Directory(filepath)
    return valid_path.filepath


def get_final_decision(mode: str, title: str, file_type: str, filepath: Path) -> str:
    """
    Prompts user for decision to proceed/cancel download

    Loops until a valid input is made

    Args:
        mode (str): Either "single", "batch", or "playlist"
        title (str): The title of the video or playlist
        file_type (str): Either "video" or "audio"
        filepath (Path): The valid directory to save the downloaded file/s

    Returns:
        str: "y", "n", or "exit"
    """
    while True:
        print(
            Fore.GREEN
            + prompts.FINAL_DECISION_PROMPT.format(
                mode=mode.upper(),
                title=title,
                file_type=file_type.title(),
                filepath=filepath,
            )
        )
        try:
            final_decision = (
                input(Fore.WHITE + "\nProceed download? y/n\n\n").strip().lower()
            )
            return validate_final_decision(final_decision)
        except ValueError:
            print(Fore.RED + '\nInvalid input. Please input "y", "n", or "exit"')
            time.sleep(DELAY)


def validate_final_decision(decision: str) -> str:
    """Validates the user's final decision

    Args:
        decision (str): The user's input

    Returns:
        str: The validated input. Either "y", "n", or "exit"

    Raises:
        ValueError: If input is not "y", "n" or "exit"
    """
    if not re.search(r"^([yn]|exit)$", decision):
        raise ValueError
    return decision


def get_url_list_file() -> Path | str:
    while True:
        print(Fore.YELLOW + prompts.GET_URL_LIST_PROMPT_1)
        try:
            return validate_url_list_file(input(Fore.WHITE + prompts.GET_URL_LIST_PROMPT_2).strip())
        except ValueError:
            print(
                Fore.RED + "\nInvalid file. Please enter a valid file or filepath",
            )
            time.sleep(DELAY)
        except FileNotFoundError:
            print(Fore.RED + "\nFile was not found. Please enter a valid file or filepath")
            time.sleep(DELAY)
        except IsADirectoryError:
            print(
                Fore.RED
                + "\nFile or filepath provided is a directory. Please enter a valid file or filepath",
            )
            time.sleep(DELAY)
        except PermissionError:
            print(
                Fore.RED + "\nYou don't have enough permission to access this file.",
            )
            time.sleep(DELAY)
        except OSError:
            print(
                Fore.RED + "\nSomething went wrong when accessing the file",
            )
            time.sleep(DELAY)
            


def validate_url_list_file(url_list_file) -> Path | str:
    if url_list_file == "exit":
        return url_list_file
    elif url_list_file == "":
        raise ValueError
    else:
        path = Path(url_list_file)
        return downloader.URL_List_File(path).filepath
    

def print_checking() -> None:
    """Prints "checking" for psuedo-loading status"""
    print(Fore.YELLOW + "\nChecking. . .\n")


def print_obj_success(title: str | None, download_mode: str) -> None:
    """Prints success with corresponding video title on successful object creation"""
    if download_mode == "single":
        print(Fore.GREEN + "Video Found!", Fore.GREEN + f"\n{title}")
    if download_mode == "batch":
        print(Fore.GREEN + f"Video Found: {title}")
    if download_mode == "playlist":
        print(Fore.GREEN + "Playlist Found!", Fore.GREEN + f"\n{title}")
        

def print_obj_fail(download_mode: str) -> None:
    """Prints failure on failed object creation"""
    if download_mode in ("single", "playlist"):
        print(
            Fore.RED
            + "\nSomething went wrong. Please check if all inputs are valid, especially the URL"
        )
    if download_mode == "batch":
        print(Fore.RED + "\nFailed to find video")


def print_success() -> None:
    """Prints success"""
    print(Fore.GREEN + "\nDownload successful!")


def print_failure() -> None:
    """Prints failure"""
    print(Fore.RED + "\nDownload failed!")


def print_dl_success() -> None:
    """Prints returning to Menu when success"""
    print(Fore.GREEN + "\nDownload success! Returning to Main Menu . . .")


def print_dl_fail() -> None:
    """Prints returning to Menu when fail"""
    print(Fore.RED + "\nDownload failed. Returning to Main Menu . . .")


def print_exception(_exception: str) -> None:
    """Prints message depending on exception"""
    if _exception == "ExtractorError":
        print(
            Fore.RED + "\nSomething went wrong when trying to extract metadata from URL"
        )
    if _exception == "DownloadError":
        print(
            Fore.RED
            + "\nSomething went wrong when trying to download. Please check your internet connection"
        )


def exit_program() -> None:
    """Prints and closes the program"""
    print(Fore.GREEN + "\nThank you for using EZ Youtube Downloader!")
    sys.exit()
