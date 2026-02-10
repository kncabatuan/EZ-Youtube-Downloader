from pathlib import Path
import re
import yt_dlp


class Download:
    GENERAL_OPTS = {"quiet": True, "no_warnings": True, "format": "bestvideo[height<=1080]+bestaudio/best[height<=1080]"}
    PLAYLIST_OPTS = {}


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
        

    def ytdlp_handler(self):
        try:
            if self.mode in ("single", "batch"):
                with yt_dlp.YoutubeDL(Download.GENERAL_OPTS) as yld:
                    return yld
            elif self.mode == "playlist":
                with yt_dlp.YoutubeDL(Download.PLAYLIST_OPTS) as yld:
                    return yld
        except (yt_dlp.utils.ExtractorError, yt_dlp.utils.DownloadError):
            raise ValueError
    

    def set_title(self):
        info = self.ytdlp_handler().extract_info(self.url, download=False)
        self.title = info["title"]


class Save_Directory:
    """Handles validation of entered filepath if any"""
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath
