from cli import prompts
from colorama import Fore
import re
import sys
import time

#Time used for delay using time.sleep (in seconds)
DELAY = 1.5


def get_user_choice() -> str:
    """
    Gets user input for Main Menu and calls validator function
    
    Returns:
        str: The validated user input   
    """
    while True:
        try:
            return validate_choice(input(Fore.WHITE + prompts.MAIN_PROMPT).strip().lower())
        except ValueError:
            print(Fore.RED + '\nInvalid input. Please enter from value 1-3 or "exit"')
            time.sleep(DELAY)
            continue


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
    if choice != "exit" and int(choice) not in range(1,4):
        raise ValueError
    return choice


def get_url() -> str:
    """
    Gets user input for URL and calls validator function

    Returns:
        str: The validated URL
    """
    while True:
        try:
            return validate_url(input(Fore.WHITE + prompts.URL_PROMPT)).strip()
        except ValueError:
            print(Fore.RED + "\nInvalid URL. Please copy-paste Youtube URL")


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
        str: The validated input for file type
    """
    while True:
        try:
            return validate_type(input(Fore.WHITE + prompts.TYPE_PROMPT).strip().lower())
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
    if file_type != "exit" and int(file_type) not in range(1,3):
        raise ValueError
    
    if file_type == "exit":
        return file_type
    if int(file_type) == 1:
        return "video"
    if int(file_type) == 2:
        return "audio"
    

def get_filepath() -> str:
    while True:
        try:
            return validate_filepath(input(Fore.WHITE + prompts.PATH_PROMPT).strip())
        except ValueError:
            print(
                Fore.RED + "\nInvalid filepath. Please follow correct format",
                Fore.RED + "\nC:\\... or C:/..."
                )


def validate_filepath(filepath: str) -> str:
    if filepath == "exit":
        return filepath
    if filepath == "" or filepath == "no":
        return "default"
    if not re.search(r"^[a-zA-Z]:[\\/].*$", filepath):
        raise ValueError
    return filepath


def print_checking():
    print(Fore.YELLOW + "\nChecking. . .\n")


def print_obj_success(title):
    print(
        Fore.GREEN + "Video Found!",
        Fore.GREEN + f"\n{title}"
        )
    

def print_obj_fail():
    print(
            Fore.RED
            + "\nThe URL that you entered is invalid. Please copy-paste the Youtube URL using your mouse for better results"
        )


def print_success() -> None:
    """Prints success"""
    print(Fore.GREEN + "\nDownload successful!")


def print_failure() -> None:
    """Prints failure"""
    print(Fore.RED + "\nDownload failed!")


def exit_program() -> None:
    """Prints and closes the program"""
    print(Fore.GREEN + "\nThank you for using EZ Youtube Downloader!")
    sys.exit()

