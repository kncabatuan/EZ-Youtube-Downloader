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
        self.mode = mode
        self.url = url
        self.file_type = file_type
        

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str) -> None:
        pattern = r"^((?:https?://)?(?:www\.|m\.)?(?:youtube\.com|youtu\.be)/(?:watch\?v=)?[\w-]{11}).*$"
        if match := re.search(pattern, url):
            if self.mode in ("single", "batch"):
                self._url = match.group(1)
            if self.mode == "playlist":
                self._url = match.group(0)
        else:
            raise ValueError


    def opts_builder(self) -> dict:
        opts = Download.BASE_OPTS

        if self.file_type == "video":
            match self.mode:
                case "single":
                    opts["noplaylist"] = True
                    opts["format"] = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
                    opts["windowsfilenames"] = True
                    opts["merge_output_format"] = "mp4"
                    opts["outtmpl"] = str(self.filepath / "%(title)s.%(ext)s")
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
            with yt_dlp.YoutubeDL(Download.BASE_OPTS) as ydl:  # type: ignore[arg-type]
                return ydl
        if caller == "download_vid":
            with yt_dlp.YoutubeDL(self.opts_builder()) as ydl:  # type: ignore[arg-type]
                return ydl
            

    def set_title(self) -> None:
        caller = "set_title"
        try:
            info = self.ytdlp_handler(caller).extract_info(self.url, download=False, process=False)
            self.title = info["title"]
        except yt_dlp.utils.ExtractorError:
            raise ValueError
        

    def save_path(self, filepath: Path) -> None:
        self.filepath = filepath


    def download_vid(self) -> None:
        caller = "download_vid"
        try:
            self.ytdlp_handler(caller).download(self.url)
        except (yt_dlp.utils.ExtractorError, yt_dlp.utils.DownloadError, yt_dlp.utils.PostProcessingError):
            raise


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
            raise NotADirectoryError
        else:
            test_file = Path(filepath) / "test_file.txt"
            try:
                test_file.touch()
                self._filepath = Path(filepath)
            except PermissionError:
                raise
            finally:
                if test_file.exists():
                    test_file.unlink()


def create_download_obj(url: str, file_type: str, mode: str) -> Download | None:
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
        download_obj = Download(url, file_type, mode)
        download_obj.set_title()
        return download_obj
    except ValueError:
        return None