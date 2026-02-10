from colorama import Fore
from helpers import downloader
from typing import Union


def create_obj(url: str, file_type: str, mode: str) -> object:
    """
    Calls downloader for only one video or audio

    Args:
        url (str): The url validated at the UI level
        file_type(str): The file type (either "video" or "audio")
        mode (str): Either "single", "batch", or "playlist"

    Returns:
        bool: True if download is successful, False otherwise
    """
    try:
        dl_object = downloader.Download(url, file_type, mode)
        dl_object.set_title()
        return dl_object
    except ValueError:
        pass


# Function to ask user for directory or save at default

# Function to Download corresponding video or audio (with loading bar)

# Return to Main Menu
