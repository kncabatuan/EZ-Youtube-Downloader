from colorama import Fore
from helpers import downloader


def download(url: str, file_type: str, mode: str) -> bool:
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
        download = downloader.Download(url, file_type, mode)
        return True
    except ValueError:
        print(
            Fore.RED
            + "\nThe URL that you enterd is invalid. Please copy-paste the Youtube URL using your mouse for better results"
        )
        return False


# Function to ask user for directory or save at default

# Function to Download corresponding video or audio (with loading bar)

# Return to Main Menu
