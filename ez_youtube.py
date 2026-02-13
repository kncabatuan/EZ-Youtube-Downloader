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
                batch_download()
            case "3":
                print("Go to playlist download")
            case "exit":
                menu.exit_program()


def get_user_inputs(download_mode) -> tuple:

    file_type = menu.get_type()
    if file_type == "exit":
        menu.exit_program()

    if download_mode in ("single", "playlist"):
        url = menu.get_url()
        if url == "exit":
            menu.exit_program()
        return url, file_type
    else:
        return file_type


def single_download():
    download_mode = "single"
    url, file_type = get_user_inputs(download_mode)

    menu.print_checking()

    if download_object := object_create(url, file_type, download_mode):
        pass
    else:
        return
    
    time.sleep(DELAY)

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


def batch_download():
    download_mode = "batch"
    file_type = get_user_inputs(download_mode)

    url_list_file = menu.get_url_list_file()
    if url_list_file == "exit":
        menu.exit_program()

    menu.print_checking()
    
    with open(url_list_file, "r") as file:
        url_list = [line.strip() for line in file]

    download_object_list = []
    for url in url_list:
        if download_object := (object_create(url, file_type, download_mode)):
            download_object_list.append(download_object)
        else:
            continue

    filepath = menu.get_filepath()
    if filepath == "exit":
        menu.exit_program()
    else:
        assert isinstance(filepath, Path)
        for download_object in download_object_list:
            download_object.save_path(filepath)

    filepath = menu.get_filepath()
    if filepath == "exit":
        menu.exit_program()
    else:
        assert isinstance(filepath, Path)
        download_object.save_path(filepath)


def object_create(url, file_type, download_mode):
    try:
        download_object = downloader.Download(url, file_type, download_mode)
        download_object.set_title()
        menu.print_obj_success(download_object.title, download_mode)
        return download_object
    except ValueError:
        menu.print_obj_fail(download_mode, url)
    




if __name__ == "__main__":
    main()
