from cli import menu
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
        match menu.get_user_choice():
            case "1":
                single_download()
            case "2":
                print("Go to batch download")
            case "3":
                print("Go to playlist download")
            case "exit":
                menu.exit_program()


def get_user_inputs() -> tuple:
    """
    Calls functions from menu module to get and validate user input

    Returns:
        tuple: The validated url and file type
    """

    url = menu.get_url()
    if url == "exit":
        menu.exit_program()

    file_type = menu.get_type()
    if file_type == "exit":
        menu.exit_program()

    return url, file_type


def single_download():
    download_mode = "single"
    url, file_type = get_user_inputs()

    menu.print_checking()

    if download_object := downloader.create_download_obj(
        url, file_type, download_mode
    ):
        menu.print_obj_success(download_object.title)
        time.sleep(DELAY)
    else:
        menu.print_obj_fail()
        time.sleep(DELAY)
        return

    filepath = menu.get_filepath()
    if filepath == "exit":
        menu.exit_program()
    else:
        assert isinstance(filepath, Path)
        download_object.save_path(filepath)

    menu.print_checking()
    time.sleep(DELAY)

    assert download_object.title is not None
    decision = menu.get_final_decision(
        download_mode, download_object.title, file_type, download_object.filepath
    )
    if decision == "y":
        try:
            download_object.download_vid()
            menu.print_dl_success()
        except yt_dlp.utils.ExtractorError:
            menu.print_exception("ExtractorError")
            menu.print_dl_fail()
        except (yt_dlp.utils.DownloadError, yt_dlp.utils.PostProcessingError):
            menu.print_exception("DownloadError")
            menu.print_dl_fail()
    elif decision == "n":
        menu.print_dl_fail()
    else:
        menu.exit_program()

    time.sleep(DELAY)
    return


if __name__ == "__main__":
    main()
