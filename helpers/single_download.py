from cli import menu
from helpers import downloader

download_mode = "single"

def download():
    URL = menu.get_url()
    type = menu.get_type()

    if URL == "exit" or type == "exit":
        menu.exit_program()

    try:
        download = downloader.Download(URL, type, download_mode)
    except:
        ...


#Function to ask user for directory or save at default

#Function to Download corresponding video or audio (with loading bar)

#Return to Main Menu