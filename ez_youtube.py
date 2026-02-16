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


def single_download():
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

    time.sleep(DELAY)

    counts = Counter([download_object.title for download_object in download_object_list])
    if duplicates := [item for item, count in counts.items() if count > 1]:
        menu.print_duplicates(duplicates)
    else:
        pass

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


def object_create(url, file_type, download_mode):
    try:
        download_object = downloader.Download(url, file_type, download_mode)
        download_object.set_title()
        return download_object
    except ValueError:
        menu.print_obj_fail(download_mode, url)


def save_path() -> Path:
    filepath = menu.get_filepath()
    if filepath == "exit":
        menu.exit_program()
    else:
        assert isinstance(filepath, Path)
        return filepath
    

def download_video(decision: str, download_mode: str, objects: downloader.Download | list) -> None:
    if decision == "y":
        try:
            menu.print_checking()
            if download_mode in ("single", "playlist"):
                objects.download_vid()
            else:
                downloaded_titles = []
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
