from cli import menu
from collections import Counter
from helpers import downloader
from pathlib import Path
import time
import yt_dlp

# Time used for delay using time.sleep (in seconds)
DELAY = 1.5


def main() -> None:
    """
    Main function for Youtube Downloader project

    Controls the flow of the program based on user answers on prompt
    """
    while True:
        try:
            match menu.get_user_choice():
                case "1":
                    single_download()
                case "2":
                    batch_download()
                case "3":
                    print("Go to playlist download")
                case "exit":
                    menu.exit_program()
        except KeyboardInterrupt:
            menu.exit_program()


def single_download() -> None:
    """Handles flow of program for single download mode"""
    download_mode = "single"
    url, file_type = get_user_inputs(download_mode)

    menu.print_checking()

    if download_object := object_create(url, file_type, download_mode):
        menu.print_obj_success(download_object.title, download_mode)
    else:
        return

    time.sleep(DELAY)

    download_object.set_path(save_path())

    menu.print_checking()
    time.sleep(DELAY)

    assert download_object.title is not None
    decision = menu.get_final_decision(
        download_mode, download_object.title, file_type, download_object.filepath
    )

    download_video(decision, download_mode, download_object)

    time.sleep(DELAY)
    return


def batch_download() -> None:
    """Handles flow of program for batch download mode"""
    download_mode = "batch"
    file_type = get_user_inputs(download_mode)[1]

    url_list_file = menu.get_url_list_file()
    if url_list_file == "exit":
        menu.exit_program()

    menu.print_checking()

    with open(url_list_file, "r") as file:
        url_list = [line.strip() for line in file]

    download_object_list = []
    detected_titles = []
    for url in url_list:
        if download_object := (object_create(url, file_type, download_mode)):
            download_object_list.append(download_object)
            if download_object.title not in detected_titles:
                menu.print_obj_success(download_object.title, download_mode)
                detected_titles.append(download_object.title)
            else:
                continue
        else:
            continue

    counts = Counter(
        [download_object.title for download_object in download_object_list]
    )
    if duplicates := [item for item, count in counts.items() if count > 1]:
        menu.print_duplicates(duplicates)

    time.sleep(DELAY)

    filepath = save_path()
    for download_object in download_object_list:
        download_object.set_path(filepath)

    menu.print_checking()
    time.sleep(DELAY)

    decision = menu.get_final_decision(
        mode=download_mode, title="Multiple", file_type=file_type, filepath=filepath
    )

    download_video(decision, download_mode, download_object_list)

    time.sleep(DELAY)
    return


def get_user_inputs(download_mode: str) -> tuple:
    """
    Gets user input for url and file type
    
    Args:
        download_mode (str): Mode of download to determine the return values

    Returns:
        tuple: If single/playlist mode, returns url and file type. If batch mode, returns file type only
    """

    file_type = menu.get_type()
    if file_type == "exit":
        menu.exit_program()

    if download_mode in ("single", "playlist"):
        url = menu.get_url()
        if url == "exit":
            menu.exit_program()
        return url, file_type
    else:
        return None, file_type


def object_create(url, file_type, download_mode) -> downloader.Download | None:
    """
    Calls on helper to create object for download. Prints appropriate message
    
    Args:
        url (str): The input URL
        file_type (str): The input file_type ("video" or "audio")
        download_mode (str): Either single, batch, or playlist (from the calling function)
    
    Returns:
        downloader.Download: The Download instance that was created
        None: If creation failed
    """
    try:
        download_object = downloader.Download(url, file_type, download_mode)
        download_object.set_title()
        return download_object
    except ValueError:
        menu.print_obj_fail(download_mode, url)
        return None


def save_path() -> Path:
    """
    Calls on cli to get the filepath to save the file, if any
    
    Returns:
        Path: The filepath
    """
    filepath = menu.get_filepath()
    if filepath == "exit":
        menu.exit_program()
    else:
        assert isinstance(filepath, Path)
        return filepath


def download_video(
    decision: str, download_mode: str, objects: downloader.Download | list
) -> None:
    """
    Calls on helper to download video or audio. Prints appropriate message
    
    Args:
        decision (str): The user decision to start download, either "y", "n" or "exit"
        download_mode (str): Either "single", "batch" or "playlist"
        objects (downloader.Download | list): Either a Download instance or a list of Download instances
    """
    if decision == "y":
        try:
            menu.print_starting_download()
            if download_mode in ("single", "playlist"):
                assert isinstance(objects, downloader.Download)
                objects.download_vid()
            else:
                downloaded_titles = []
                assert isinstance(objects, list)
                for object in objects:
                    if object.title not in downloaded_titles:
                        object.download_vid()
                        downloaded_titles.append(object.title)
                    else:
                        continue
            menu.print_dl_success()
            return
        except yt_dlp.utils.ExtractorError:
            menu.print_exception("ExtractorError")
            menu.print_dl_fail()
            return
        except (yt_dlp.utils.DownloadError, yt_dlp.utils.PostProcessingError):
            menu.print_exception("DownloadError")
            menu.print_dl_fail()
            return
        except KeyboardInterrupt:
            menu.print_exception("KeyboardInterrupt")
            menu.print_dl_fail()
            return
    elif decision == "n":
        menu.print_dl_fail()
        return
    else:
        menu.exit_program()


if __name__ == "__main__":
    main()
