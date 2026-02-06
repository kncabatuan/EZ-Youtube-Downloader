from pathlib import Path
import re


class Download:
    """Handles downloading of Youtube video or audio"""
    def __init__(self, url: str, file_type: str, mode: str) -> None:
        self.url = url
        self.file_type = file_type
        self.mode = mode

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str) -> None:
        pattern = r"^((?:https?://)?(?:www\.|m\.)?(?:youtube\.com|youtu\.be)/(?:watch\?v=)?[\w-]{11}).*$"
        if match := re.search(pattern, url):
            self._url = match.group(1)
        else:
            raise ValueError


class Save_Directory:
    """Handles validation of entered filepath if any"""
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath
