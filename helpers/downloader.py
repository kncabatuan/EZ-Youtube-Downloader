from pathlib import Path


# Class for Youtube URL
class Download:
    def __init__(self, url: str, type: str, mode: str) -> None:
        self.url = url
        self.type = type
        self.mode = mode

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str) -> None:
        pattern = r"^(?:https?://)?(?:www\.|m\.)?(?:youtube\.com|youtu\.be)/
        # Insert validation here for URL
        self._url = url


# Class for file-name
class Save_Directory:
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath
