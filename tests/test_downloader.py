from helpers import downloader
from pathlib import Path
import pytest

def test_download_init():
    valid_url = "https://www.youtube.com/watch?v=testtesttes"
    valid_type = "video"
    valid_mode = "single"
    test_valid_obj = downloader.Download(valid_url, valid_type, valid_mode)

    assert test_valid_obj.url == valid_url
    assert test_valid_obj.file_type == valid_type
    assert test_valid_obj.mode == valid_mode

    invalid_url = "https://www.youtube.com/watch?v=testtest&list=test&index=1"

    with pytest.raises(ValueError):
        downloader.Download(invalid_url, valid_type, valid_mode)


def test_url_extraction():
    valid_url = "https://www.youtube.com/watch?v=testtesttes&list=test&index=test"
    valid_type = "video"
    modes = ("single", "batch", "playlist")

    test_obj = downloader.Download(valid_url, valid_type, modes[0])
    assert test_obj.url == "https://www.youtube.com/watch?v=testtesttes"

    test_obj = downloader.Download(valid_url, valid_type, modes[1])
    assert test_obj.url == "https://www.youtube.com/watch?v=testtesttes"

    test_obj = downloader.Download(valid_url, valid_type, modes[2])
    assert test_obj.url == "https://www.youtube.com/watch?v=testtesttes&list=test&index=test"


def test_opts_builder():
    valid_url = "https://www.youtube.com/watch?v=testtesttes&list=test&index=test"
    valid_types = ("video", "audio")
    mode = "single"
    filepath = Path("test_filepath")

    test_obj1 = downloader.Download(valid_url, valid_types[0], mode)
    test_obj1.filepath = filepath
    assert test_obj1.opts_builder() == {
        "quiet": True,
        "no_warnings": True,
        "windowsfilenames": True,
        "noplaylist": True,
        "format": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "merge_output_format": "mp4",
        "outtmpl": str(test_obj1.filepath / "%(title)s.%(ext)s")
    }

    test_obj2 = downloader.Download(valid_url, valid_types[1], mode)
    test_obj2.filepath = filepath
    assert test_obj2.opts_builder() == {
        "quiet": True,
        "no_warnings": True,
        "windowsfilenames": True,
        "noplaylist": True,
        "format": "bestaudio/best",
        "outtmpl": str(test_obj2.filepath / "%(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]
    }

