from pathlib import Path
from typing import Any
import re
import yt_dlp


class MyLogger:
    def debug(self, msg):
        pass
    
    def warning(self, msg):
        pass

    def error(self, msg):
        pass

def my_hook(d):
    if d["status"] == "error":
        pass
    if d["status"] == "downloading":
        filename = Path(d.get("filename")).name
        total = d.get("total_bytes") or d.get("total_bytes_estimate")
        downloaded = d.get("downloaded_bytes", 0)

        if total:
            percent = downloaded / total * 100
            print(f"\rDownloading {filename}: {percent:.2f}%", end="")

class Download:
    """Handles downloading of Youtube video or audio"""

    # Base options used for YoutubeDL
    BASE_OPTS: dict[str, Any] = {
        "quiet": True,
        "no_warnings": True,
        "windowsfilenames": True,
        "logger": MyLogger(),
        "progress_hooks": [my_hook]
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
        """
        URL validation

        Args:
            url (str): The input URL

        Raises:
            ValueError: If input URL does not match regex pattern
        """
        pattern = r"^((https?://)?(?:www\.|m\.)?(?:youtube\.com|youtu\.be)/(?:watch\?v=)?[\w-]{11}).*$"
        if match := re.search(pattern, url):
            if self.mode in ("single", "batch"):
                if match.group(2) == None:
                    self._url = "https://" + match.group(1)
                else:
                    self._url = match.group(1)
            if self.mode == "playlist":
                if match.group(2) == None:
                    self._url = "https://" + match.group(0)
                else:
                    self._url = match.group(0)
        else:
            raise ValueError

    def opts_builder(self) -> dict:
        """
        Builds options for downloading using YoutubeDL

        Returns:
            dict: The updated options (started from base opts) depending on download mode and type
        """
        opts = Download.BASE_OPTS.copy()

        if self.file_type == "video":
            match self.mode:
                case "single":
                    opts["noplaylist"] = True
                    opts["format"] = (
                        "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
                    )
                    opts["merge_output_format"] = "mp4"
                    opts["outtmpl"] = str(self.filepath / "%(title)s.%(ext)s")
                case "batch":
                    ...
                case "playlist":
                    ...
        elif self.file_type == "audio":
            match self.mode:
                case "single":
                    opts["noplaylist"] = True
                    opts["format"] = "bestaudio/best"
                    opts["outtmpl"] = str(self.filepath / "%(title)s.%(ext)s")
                    opts["postprocessors"] = [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": "mp3",
                            "preferredquality": "192",
                        }
                    ]
                case "batch":
                    ...
                case "playlist":
                    ...

        return opts

    def ytdlp_handler(self, caller: str) -> yt_dlp.YoutubeDL:
        """
        Creates YoutubeDL object based on caller function

        Args:
            caller (str): Sets caller of this function to pass the correct options to YoutubeDL

        Returns:
            yt_dlp.YoutubeDL: The YoutubeDL object

        Raises:
            ValueError: If caller not in set tuple (not applicable)
        """
        if not caller in ("set_title", "download_vid"):
            raise ValueError

        if caller == "set_title":
            with yt_dlp.YoutubeDL(Download.BASE_OPTS) as ydl:  # type: ignore[arg-type]
                return ydl
        else:
            with yt_dlp.YoutubeDL(self.opts_builder()) as ydl:  # type: ignore[arg-type]
                return ydl

    def set_title(self) -> None:
        """
        Sets the title attribute of the Download object

        Raises:
            ValueError: If extraction of metadata fails
        """
        caller = "set_title"
        try:
            info = self.ytdlp_handler(caller).extract_info(
                self.url, download=False, process=False
            )
            if "title" not in info.keys():
                raise ValueError
            self.title = info["title"]
        except (yt_dlp.utils.ExtractorError, yt_dlp.utils.DownloadError):
            raise ValueError

    def save_path(self, filepath: Path) -> None:
        """
        Adds filepath attribute to the created Download object

        Args:
            filepath (Path): The file path where the user wants to save their downloads
        """
        self.filepath = filepath

    def download_vid(self) -> None:
        """
        Downloads the video/audio using YoutubeDL

        Raises:
            yt_dlp.utils.ExtractorError: If extraction of metadata fails
            yt_dlp.utils.DownloadError: If download fails due to connection errors or link issues
            yt_dlp.utils.PostProcessingError: If conversion, if any, fails
        """
        caller = "download_vid"
        try:
            self.ytdlp_handler(caller).download(self.url)
        except (
            yt_dlp.utils.ExtractorError,
            yt_dlp.utils.DownloadError,
            yt_dlp.utils.PostProcessingError,
        ):
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
        """
        Filepath validation

        Args:
            filepath(str): The user input for URL

        Raises:
            ValueError: If input does not match regex pattern as initial check
            NotADirectoryError: If input is not a directory
            PermissionError: If the user does not have enough permission to access directory
            OSError: If other OS-related error occurs
        """
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


class URL_List_File:
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, filepath):
        if not filepath.exists():
            raise FileNotFoundError
        elif filepath.is_dir():
            raise IsADirectoryError
        elif filepath.suffix.lower() != ".txt":
            raise ValueError
        else:
            try:
                with filepath.open("r"):
                    pass
            except PermissionError:
                raise
            except OSError:
                raise

        self._filepath = filepath