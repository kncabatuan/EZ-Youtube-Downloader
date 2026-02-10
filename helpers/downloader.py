from pathlib import Path
from typing import Any
import re
import yt_dlp


class Download:
    """Handles downloading of Youtube video or audio"""

    GENERAL_OPTS = {
        "quiet": True,
        "no_warnings": True,
        "format": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    }
    PLAYLIST_OPTS: dict[str, Any] = {}


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

    def ytdlp_handler(self) -> yt_dlp.YoutubeDL:
        if self.mode in ("single", "batch"):
            with yt_dlp.YoutubeDL(Download.GENERAL_OPTS) as yld:  # type: ignore[arg-type]
                return yld
        elif self.mode == "playlist":
            with yt_dlp.YoutubeDL(Download.PLAYLIST_OPTS) as yld:  # type: ignore[arg-type]
                return yld
        else:
            raise ValueError

    def set_title(self) -> None:
        try:
            info = self.ytdlp_handler().extract_info(self.url, download=False)
            self.title = info["title"]
        except (yt_dlp.utils.ExtractorError, yt_dlp.utils.DownloadError):
            raise ValueError


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
        elif not Path(filepath).exists():
            raise ValueError
        else:
            self._filepath = Path(filepath)
