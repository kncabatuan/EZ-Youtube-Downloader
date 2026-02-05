from cli import menu
from helpers import single_download
import time

DELAY = 1.5


def main() -> None:
    while True:
        match menu.get_user_choice():
            case "1":
                if single_download.download():
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


if __name__ == "__main__":
    main()