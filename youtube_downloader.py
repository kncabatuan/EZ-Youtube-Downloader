from cli import menu
from helpers import single_download
import time

#Time used for delay using time.sleep (in seconds)
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
                if single_download.download(url, file_type, download_mode):
                    menu.print_success()
                else:
                    menu.print_failure()
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