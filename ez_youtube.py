from cli import menu
from helpers import single_download
import time

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
                url, file_type = get_user_inputs()
                download_mode = "single"
                menu.print_checking()

                if dl_obj := single_download.create_obj(url, file_type, download_mode):
                    menu.print_obj_success(dl_obj.title)
                    time.sleep(DELAY)
                else:
                    menu.print_obj_fail()
                    time.sleep(DELAY)
                    continue

                filepath = menu.get_filepath()
                if filepath == "exit":
                    menu.exit_program()
                
                menu.print_checking()
                time.sleep(DELAY)

                decision = menu.get_final_decision(download_mode, dl_obj.title, file_type, filepath)
                if decision == "y":
                    single_download
                    menu.print_dl_success()
                elif decision == "n":
                    menu.print_dl_fail()
                else:
                    menu.exit_program()

            case "2":
                print("Go to batch download")
            case "3":
                print("Go to playlist download")
            case "exit":
                menu.exit_program()

        time.sleep(DELAY)


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


if __name__ == "__main__":
    main()
