from pathlib import Path
from typing import Any
import re
import yt_dlp


class Download:
    """Handles downloading of Youtube video or audio"""

    BASE_OPTS = {
        "quiet": True,
        "no_warnings": True,
        "windowsfilenames": True
    }

    def __init__(self, url: str, file_type: str, mode: str) -> None:
        self.url = url
        self.file_type = file_type
        self.mode = mode

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str) -> None:
        pattern = r"^(?:https?://)?(?:www\.|m\.)?(?:youtube\.com|youtu\.be)/(?:watch\?v=)?[\w-]{11}.*$"
        if match := re.search(pattern, url):
            self._url = match.group()
        else:
            raise ValueError


    def opts_builder(self) -> dict:
        opts = Download.BASE_OPTS

        if self.file_type == "video":
            match self.mode:
                case "single":
                    opts["noplaylist"] = True
                    opts["format"] = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
                case "batch":
                    ...
                case "playlist":
                    ...
        elif self.file_type == "audio":
            match self.mode:
                case "single":
                    ...
                case "batch":
                    ...
                case "playlist":
                    ...

        return opts

    def ytdlp_handler(self, caller: str) -> yt_dlp.YoutubeDL:
        if caller == "set_title":
            with yt_dlp.YoutubeDL(Download.BASE_OPTS) as yld:  # type: ignore[arg-type]
                return yld
        if caller == "download_vid":
            with yt_dlp.YoutubeDL(Download.opts_builder) as yld:  # type: ignore[arg-type]
                return yld
            

    def set_title(self) -> None:
        caller = "set_title"
        try:
            info = self.ytdlp_handler(caller).extract_info(self.url, download=False)
            self.title = info["title"]
        except (yt_dlp.utils.ExtractorError, yt_dlp.utils.DownloadError):
            raise ValueError


    def download_vid(self, ) -> None:
        ...


class Save_Directory:
    """Handles validation of entered filepath if any"""

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath

    @property
    def filepath(self) -> Path:
        return self._filepath

    @filepath.setter
    def filepath(self, filepath: str) -> None:
        if filepath in ("", "no"):
            self._filepath = Path.cwd()
        elif not re.search(r"^[a-zA-Z]:[\\/].*$", filepath):
            raise ValueError
        elif not Path(filepath).is_dir():
            raise ValueError
        else:
            self._filepath = Path(filepath)


def create_obj(url: str, file_type: str, mode: str) -> Download | None:
    """
    Calls downloader for only one video or audio

    Args:
        url (str): The url validated at the UI level
        file_type(str): The file type (either "video" or "audio")
        mode (str): Either "single", "batch", or "playlist"

    Returns:
        bool: True if download is successful, False otherwise
    """
    try:
        dl_object = Download(url, file_type, mode)
        dl_object.set_title()
        return dl_object
    except ValueError:
        return None