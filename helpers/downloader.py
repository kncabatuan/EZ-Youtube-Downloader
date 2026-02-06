from pathlib import Path
import re


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
        pattern = r"^((?:https?://)?(?:www\.|m\.)?(?:youtube\.com|youtu\.be)/(?:watch?v=)?[/w-]{11}).*$)"
        if match := re.search(pattern, url):
            url = match.group(1)

        self._url = url


# Class for file-name
class Save_Directory:
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath
