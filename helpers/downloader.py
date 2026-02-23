from pathlib import Path
from typing import Any
import re
import shutil
import sys
import yt_dlp

# The root program directory
if getattr(sys, "frozen", False):
    PROGRAM_DIR = Path(sys.executable).parent
else:
    PROGRAM_DIR = Path(__file__).parent.parent


# Used to override default yt-dlp printing to terminal
class MyLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


# Used for properly printing hook
LAST_PERCENT = -1


def my_hook(d: dict[str, Any]) -> None:
    """
    Progress hook used

    Args:
        d (dict): The dictionary passed by yt-dlp
    """

    # Used for proper printing of hook
    global LAST_PERCENT

    terminal_width = shutil.get_terminal_size().columns

    if d["status"] == "error":
        pass
    elif d["status"] == "finished":
        LAST_PERCENT = -1
        print("")
    elif d["status"] == "downloading":
        raw_filename = d.get("filename")

        assert isinstance(raw_filename, str)
        filename = Path(raw_filename).stem

        if match := re.search(r"\.f(\d{3})", filename):
            if int(match.group(1)) >= 300:
                message_prefix = "Downloading Video for"
            else:
                message_prefix = "Downloading Audio for"

            filename = filename.strip(f".f{match.group(1)}")
        else:
            message_prefix = "Downloading"

        total = d.get("total_bytes") or d.get("total_bytes_estimate")
        downloaded = d.get("downloaded_bytes", 0)

        if total:
            percent = downloaded / total * 100

            if percent != LAST_PERCENT:
                LAST_PERCENT = percent

                base_text = f"{message_prefix} {filename}: {percent:.2f}%"
                if len(base_text) >= terminal_width:
                    fixed_text = f"{message_prefix} : {percent:.2f}%"
                    allowed = terminal_width - len(fixed_text) - 6
                    new_filename = f"{filename[:max(0,allowed)]}..."
                    rewrite_line(f"{message_prefix} {new_filename}: {percent:.2f}%")
                else:
                    rewrite_line(base_text)


def rewrite_line(text: str) -> None:
    """
    Helper function for the progress hook

    Args:
        text (str): The message to print with the appropriate download progress and file name
    """
    print("\r\033[K" + text, end="", flush=True)


class Download:
    """Handles downloading of Youtube video or audio"""

    # Base options used for YoutubeDL
    BASE_OPTS: dict[str, Any] = {
        "quiet": True,
        "no_warnings": True,
        "windowsfilenames": True,
        "logger": MyLogger(),
        "progress_hooks": [my_hook],
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

        if self.ffmpeg_location is None:
            pass
        else:
            opts["ffmpeg_location"] = str(self.ffmpeg_location)

        if self.file_type == "video":
            opts["noplaylist"] = True
            opts["format"] = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
            opts["merge_output_format"] = "mp4"
            opts["outtmpl"] = str(self.filepath / "%(title)s.%(ext)s")

        elif self.file_type == "audio":
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

        if caller in ("set_title"):
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

    def set_path(self) -> None:
        """
        Adds filepath attribute to Download object

        Raises:
            PermissionError: If user does not have enough permission to access the downloads folder
            OSError: If other os-related error occurs
        """

        default_save_path = Path.home() / "Downloads"
        if not default_save_path.exists():
            try:
                default_save_path.mkdir(exist_ok=True)
            except (PermissionError, OSError):
                raise

        test_file = default_save_path / "test_file.txt"
        try:
            test_file.touch()
            self.filepath = default_save_path
        except PermissionError:
            raise
        finally:
            if test_file.exists():
                test_file.unlink()

    def set_ffmpeg_location(self, ffmpeg_location: Path | None) -> None:
        """
        Adds ffmpeg_location attribute to created Download object

        Args:
            ffmpeg_location (Path | None): Path of the ffmpeg bin folder if ffmpeg is not in PATH, None otherwise
        """
        self.ffmpeg_location = ffmpeg_location

    def download_vid(self) -> None:
        """
        Downloads the video/audio using YoutubeDL

        Raises:
            yt_dlp.utils.ExtractorError: If extraction of metadata fails
            yt_dlp.utils.DownloadError: If download fails due to connection errors or link issues
            yt_dlp.utils.PostProcessingError: If conversion, if any, fails
            KeyboardInterrupt: If user uses Ctrl+C during the run
        """
        caller = "download_vid"
        try:
            self.ytdlp_handler(caller).download(self.url)
        except (
            yt_dlp.utils.ExtractorError,
            yt_dlp.utils.DownloadError,
            yt_dlp.utils.PostProcessingError,
            KeyboardInterrupt,
        ):
            raise


class URL_List_File:
    """Sets filepath attribute for URL_List_File"""

    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath

    @property
    def filepath(self):
        return self._filepath

    @filepath.setter
    def filepath(self, filepath: Path):
        """
        Txt file path validation.

        Args:
            filepath (Path): The path for the txt file

        Raises:
            FileNotFoundError: If the file cannot be found
            IsADirectoryError: If the path points to a directory
            PermissionError: If the user does not have permission to access that file
            OSError: If other OS-related error occurred
        """
        if not filepath.exists():
            raise FileNotFoundError
        elif filepath.is_dir():
            raise IsADirectoryError
        else:
            try:
                with filepath.open("r"):
                    pass
            except PermissionError:
                raise
            except OSError:
                raise

        self._filepath = filepath
