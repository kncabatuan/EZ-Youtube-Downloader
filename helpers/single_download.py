from helpers import downloader

def download(url: str, type: str, mode: str):
    try:
        download = downloader.Download(url, type, mode)
        print(download.url)
        print(download.type)
        print(download.mode)
        return True
    except Exception:
        return False


#Function to ask user for directory or save at default

#Function to Download corresponding video or audio (with loading bar)

#Return to Main Menu