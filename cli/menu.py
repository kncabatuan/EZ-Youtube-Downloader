from cli import prompts
from colorama import Fore
from helpers import downloader
from pathlib import Path
from typing import NoReturn
import re
import shutil
import sys
import time

# Time used for delay using time.sleep (in seconds)
DELAY_SHORT = 1.5
DELAY_LONG = 2

# Used for printing horizontal lines in terminal for UX
COLUMNS = shutil.get_terminal_size().columns


def get_user_choice() -> str:
    """
    Gets user input for Main Menu and calls validator function.

    Loops until a valid choice or "exit" is obtained.

    Returns:
        str: The validated user input
    """
    while True:
        print(Fore.WHITE + ("\n" + ("-" * COLUMNS)))
        print(Fore.YELLOW + prompts.MAIN_PROMPT_1)
        try:
            return validate_choice(
                input(Fore.WHITE + prompts.MAIN_PROMPT_2).strip().lower()
            )
        except ValueError:
            print(Fore.RED + '\nInvalid input. Please enter "1", "2" or "exit"')
            time.sleep(DELAY_SHORT)


def validate_choice(choice: str) -> str:
    """
    Validates user input from caller

    Args:
        choice (str): The user input

    Returns:
        str: The validated choice ("1", "2" or "exit")

    Raises:
        ValueError: If choice is not "1", "2" or "exit"
    """
    if choice != "exit" and int(choice) not in (1, 2):
        raise ValueError
    return choice


def get_url() -> str:
    """
    Gets user input for URL and calls validator function.

    Loops until a valid (UI-level) url or "exit"/"cancel" is obtained.

    Returns:
        str: The validated URL
    """
    while True:
        print(Fore.WHITE + ("\n" + ("-" * COLUMNS)))
        print(Fore.YELLOW + prompts.URL_PROMPT)
        try:
            return validate_url(input(Fore.WHITE + "")).strip()
        except ValueError:
            print(
                Fore.RED
                + '\nInvalid URL. Please copy-paste Youtube URL, enter "cancel", or "exit"'
            )
            time.sleep(DELAY_SHORT)


def validate_url(url: str) -> str:
    """
    Validates user input from caller

    Args:
        url (str): The user's URL input

    Returns:
        str: The validated URL, "exit", or "cancel"

    Raises:
        ValueError: If input is empty, regex is not recognized in input, or input is not exit/cancel
    """
    pattern = r"^(?:https?://)?(?:www\.|m\.)?(?:youtube\.com|youtu\.be)/"
    if url.lower() not in ("exit", "cancel") and not re.search(pattern, url):
        raise ValueError

    if url == "":
        raise ValueError

    return url


def get_type() -> str:
    """
    Gets user input for File Type and calls validator function.

    Loops until a valid type or "exit"/"cancel" is obtained.

    Returns:
        str: The file type ("video"/"audio"), "exit", or "cancel"
    """
    while True:
        print(Fore.WHITE + ("\n" + ("-" * COLUMNS)))
        print(Fore.YELLOW + prompts.TYPE_PROMPT_1)
        try:
            return validate_type(
                input(Fore.WHITE + prompts.TYPE_PROMPT_2).strip().lower()
            )
        except ValueError:
            print(Fore.RED + '\nInvalid input. Please enter 1, 2, "cancel", or "exit"')
            time.sleep(DELAY_SHORT)


def validate_type(file_type: str) -> str:
    """
    Validates user input from caller

    Args:
        file_type (str): The user's file_type input

    Returns:
        str: The validated file_type ("video" or "audio"), "cancel, or "exit"

    Raises:
        ValueError: If input is not "1", "2", "cancel", or "exit"
    """
    if file_type not in ("exit", "cancel") and int(file_type) not in range(1, 3):
        raise ValueError

    if file_type in ("exit", "cancel"):
        return file_type
    if int(file_type) == 1:
        return "video"
    if int(file_type) == 2:
        return "audio"

    raise ValueError


def get_final_decision(mode: str, title: str, file_type: str, filepath: Path) -> str:
    """
    Prompts user for decision to proceed/cancel download

    Loops until a valid input is made

    Args:
        mode (str): Either "single" or "batch"
        title (str): The title of the video
        file_type (str): Either "video" or "audio"
        filepath (Path): The valid directory to save the downloaded file/s

    Returns:
        str: "y", "n", "cancel", or "exit"
    """
    while True:
        print(Fore.WHITE + ("\n" + ("-" * COLUMNS)))
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
            if mode == "single":
                final_decision = (
                    input(Fore.YELLOW + "\nProceed download? y/n\n\n").strip().lower()
                )
            else:
                final_decision = (
                    input(
                        Fore.YELLOW
                        + "\nProceed download? Videos that were not found will be skipped. y/n\n\n"
                    )
                    .strip()
                    .lower()
                )
            print("")
            return validate_decision(final_decision)
        except ValueError:
            print(
                Fore.RED + '\nInvalid input. Please input "y", "n", "cancel", or "exit"'
            )
            time.sleep(DELAY_SHORT)


def validate_decision(decision: str) -> str:
    """
    Validates the user's final decision

    Args:
        decision (str): The user's input

    Returns:
        str: The validated input. Either "y", "n", "cancel", or "exit"

    Raises:
        ValueError: If input is not "y", "n", "cancel", or "exit"
    """
    if not re.search(r"^([yn]|exit|cancel)$", decision):
        raise ValueError
    return decision


def get_url_list_file() -> Path | str:
    """
    Shows instruction on how to use batch file

    Gets user input once they followed the said instructions

    Returns:
        Path: The validated path of the text file on the desktop
        str: "exit" or "cancel"
    """
    while True:
        print(Fore.WHITE + ("\n" + ("-" * COLUMNS)))
        print(Fore.YELLOW + prompts.GET_URL_LIST_PROMPT_1)
        try:
            valid_file = validate_url_list_file_input(
                input(Fore.WHITE + prompts.GET_URL_LIST_PROMPT_2).strip().lower()
            )
            if isinstance(valid_file, Path):
                with open(valid_file, "r") as file:
                    url_list = [line.strip() for line in file]
                    if not url_list:
                        print_empty_file()
                        time.sleep(DELAY_SHORT)
                        continue
                    else:
                        return valid_file
        except ValueError:
            print(
                Fore.RED
                + '\nInvalid input. Please enter "proceed", "cancel", or "exit".',
            )
            time.sleep(DELAY_SHORT)
        except FileNotFoundError:
            print(
                Fore.RED
                + '\nFile was not found. Make sure that it is in DESKTOP and named "ez"'
            )
            time.sleep(DELAY_SHORT)
        except IsADirectoryError:
            print(
                Fore.RED
                + "\nFile provided is a directory. Please make sure it is a .txt file"
            )
            time.sleep(DELAY_SHORT)
        except PermissionError:
            print(
                Fore.RED + "\nYou don't have enough permission to access this file.",
            )
            time.sleep(DELAY_SHORT)
        except OSError:
            print(
                Fore.RED + "\nSomething went wrong when accessing the file",
            )
            time.sleep(DELAY_SHORT)


def validate_url_list_file_input(url_list_file_input: str) -> Path | str:
    """
    Validates the user's input in getting url list file

    Args:
        url_list_file_input (str): The user input

    Returns:
        Path: The validated path of the text file
        str: Either "proceed", "cancel", or "exit"

    Raises:
        ValueError: If the input is not "proceed" or "exit"
        FileNotFoundError: If the text file is not found in Desktop
        IsADirectoryError: if the file detected is a directory
        PermissionError: If the user does not have enough permission to access the file
        OSError: If other os-related error occurs
    """

    if url_list_file_input not in ("proceed", "cancel", "exit"):
        raise ValueError
    elif url_list_file_input in ("exit", "cancel"):
        return url_list_file_input
    else:
        path = Path.home() / "Desktop" / "ez.txt"
        return downloader.URL_List_File(path).filepath


def get_dependency_decision() -> str:
    """
    Gets the user's decision on ffmpeg dependency

    Loops until a valid decision is entered

    Returns:
        str: The validated decison. Either "y", "n", "cancel", or "exit"
    """
    while True:
        try:
            return validate_decision(
                input(Fore.BLUE + prompts.MISSING_DEPENDENCY_PROMPT).strip()
            )
        except ValueError:
            print(
                Fore.RED + '\nInvalid input. Please input "y", "n", "cancel" or "exit"'
            )
            time.sleep(DELAY_SHORT)


def print_starting_program() -> None:
    """Prints message at program run"""
    print(Fore.WHITE + ("\n" + ("-" * COLUMNS)))
    print(Fore.YELLOW + "\nStarting EZ Youtube v1.0 . . .")
    time.sleep(DELAY_SHORT)
    print(Fore.YELLOW + "\nChecking for dependencies. . .")
    time.sleep(DELAY_SHORT)


def print_checking() -> None:
    """Prints "checking" for psuedo-loading status"""
    print(Fore.YELLOW + "\nChecking. . .\n")


def print_obj_success(title: str | None, download_mode: str) -> None:
    """Prints success with corresponding video title on successful object creation"""
    if download_mode == "single":
        print(Fore.GREEN + "Video Found!", Fore.GREEN + f"\n{title}")
    if download_mode == "batch":
        print(Fore.GREEN + f"Video Found: {title}")


def print_obj_fail(download_mode: str, url: str) -> None:
    """Prints failure on failed object creation"""
    if download_mode == "single":
        print(
            Fore.RED
            + "\nSomething went wrong. Please check if all inputs are valid, especially the URL"
        )
    if download_mode == "batch":
        print(Fore.RED + f"Failed to find video from {url}")


def print_dl_success(caller: str) -> None:
    assert caller in ("system_check", "download")
    if caller == "system_check":
        print(Fore.GREEN + "\n\nDownload success!")
    else:
        print(Fore.GREEN + "\n\nDownload success! It's in your DOWNLOADS folder. :)")


def print_dl_fail() -> None:
    """Prints returning to Menu when fail"""
    print(Fore.RED + "\nDownload failed. Returning to Main Menu . . .")


def print_exception(
    _exception: str, filename: str | None = None, request_error: bool | None = None
) -> None:
    """
    Prints message depending on exception

    Args:
        filename (str|None): Name of the video. Used only if it is detected in the Downloads folder before download
        request_error (bool): True if the call was from ffmpeg downloading, False by default
    """
    if _exception == "FileExistsError":
        print(Fore.BLUE + f"\n{filename} is already in your downloads folder")
    if _exception == "ExtractorError":
        print(
            Fore.RED + "\nSomething went wrong when trying to extract metadata from URL"
        )
    if _exception == "DownloadError":
        print(
            Fore.RED
            + "\n\nSomething went wrong. Make sure you have stable internet connection"
        )
        print(
            Fore.RED
            + "\nIf internet is stable, possible issues are regional restriction, members-only content, or official music/VEVO videos."
        )
    if _exception == "KeyboardInterrupt":
        print(Fore.RED + "\n\nDownload has been interrupted")
    if _exception == "PermissionError":
        print(Fore.RED + "\n\nYou may not have permission to access this folder.")
    if _exception == "RequestException":
        print(
            Fore.RED
            + "\n\nSomething went wrong when trying to access the website. Make sure you have stable internet connection."
        )
    if _exception == "OSError":
        if request_error == True:
            print(
                Fore.RED
                + "\n\nAn error occurred! Make sure you have stable internet connection"
            )
        else:
            print(Fore.RED + "\n\nAn OS-related error occurred!")
    if _exception == "zipfile.BadZipFile":
        print(
            Fore.RED
            + "\n\nThe downloaded zip file is corrupted or incomplete. Make sure you have stable internet connection"
        )


def print_duplicates(duplicates: list) -> None:
    """Prints message if duplicate titles are detected from batch downloading"""
    print(
        Fore.BLUE
        + "\n\nDuplicates detected! The following will only be downloaded once:\n"
    )
    for item in duplicates:
        print(Fore.BLUE + f"{item}")


def print_starting_download(caller: str) -> None:
    """Prints appropriate download start message depending on caller"""
    assert caller in ("system_check", "download")
    if caller == "system_check":
        print(
            Fore.YELLOW
            + "\nStarting download. Please be patient. This may take a while. . .\n"
        )
    else:
        print(
            Fore.YELLOW + "\nStarting download. Wait until it says success or failure."
        )
        print(Fore.YELLOW + "Please be patient. . .")
        print(Fore.YELLOW + "\nYou can interrupt download with Ctrl + C\n")


def print_dependency_message() -> None:
    """Prints message if user does not want to download ffmpeg"""
    print(Fore.YELLOW + prompts.DEPENDENCY_MESSAGE)


def print_cancel(mode: str) -> None:
    """
    Prints message if the user enters cancel

    Args:
        mode (str): Either "single" or "batch"
    """
    print(
        Fore.RED + f"\n{mode.title()} Download canceled. Returning to Main Menu . . ."
    )


def print_empty_file():
    """Prints message that url list file is empty"""
    print(Fore.RED + f"\nThe text file is empty. Make sure you put at least one URL")


def print_no_downloadable_url_detected():
    """Prints message that no downloadable object is detected"""
    print(Fore.RED + f"\nFailed to detect a video that is downloadable")


def exit_program() -> NoReturn:
    """Prints and closes the program"""
    print(Fore.GREEN + "\nThank you for using EZ Youtube Downloader!")
    time.sleep(DELAY_LONG)
    sys.exit()
