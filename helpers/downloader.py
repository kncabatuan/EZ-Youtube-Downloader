from pathlib import Path
import re
import yt_dlp


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
        

    def set_video_name(self):
        opts = {"quiet": True, "no_warnings": True}
        try:
            with yt_dlp.YoutubeDL(opts) as yld:
                info = yld.extract_info(self.url, download=False)
                self.video_name = info["title"]
        except (yt_dlp.utils.ExtractorError, yt_dlp.utils.DownloadError):
            raise ValueError


class Save_Directory:
    """Handles validation of entered filepath if any"""
    def __init__(self, filepath: Path) -> None:
        self.filepath = filepath
