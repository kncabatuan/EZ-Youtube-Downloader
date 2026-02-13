from helpers import downloader
from pathlib import Path
from unittest.mock import patch, MagicMock
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
    opts1 = test_obj1.opts_builder()

    assert opts1["quiet"] == True
    assert opts1["no_warnings"] == True
    assert opts1["windowsfilenames"] == True
    assert isinstance(opts1["logger"], downloader.MyLogger)
    assert opts1["noplaylist"] == True
    assert opts1["format"] == "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
    assert opts1["merge_output_format"] == "mp4"
    assert opts1["outtmpl"] == str(test_obj1.filepath / "%(title)s.%(ext)s")


    test_obj2 = downloader.Download(valid_url, valid_types[1], mode)
    test_obj2.filepath = filepath
    opts2 = test_obj2.opts_builder()

    assert opts2["quiet"] == True
    assert opts2["no_warnings"] == True
    assert opts2["windowsfilenames"] == True
    assert isinstance(opts2["logger"], downloader.MyLogger)
    assert opts2["noplaylist"] == True
    assert opts2["format"] == "bestaudio/best"
    assert opts2["outtmpl"] == str(test_obj2.filepath / "%(title)s.%(ext)s")
    assert opts2["postprocessors"] == [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]


def test_data_extraction():
    valid_url = "https://www.youtube.com/watch?v=testtesttes"
    valid_type = "video"
    valid_mode = "single"

    with patch("helpers.downloader.yt_dlp.YoutubeDL") as mock_ydl:
        mock_instance = MagicMock()
        mock_ydl.return_value.__enter__.return_value = mock_instance

        mock_instance.extract_info.return_value = {"title": "Test Title"}

        test_obj = downloader.Download(valid_url, valid_type, valid_mode)
        test_obj.set_title()

        mock_instance.extract_info.assert_called_once_with(valid_url, download=False, process=False)
        assert test_obj.title == "Test Title"


def test_download():
    valid_url = "https://www.youtube.com/watch?v=testtesttes"
    valid_type = "video"
    valid_mode = "single"
    valid_filepath = Path("test_filepath")

    with patch("helpers.downloader.yt_dlp.YoutubeDL") as mock_ydl:
        mock_instance = MagicMock()
        mock_ydl.return_value.__enter__.return_value = mock_instance

        test_obj = downloader.Download(valid_url, valid_type, valid_mode)
        test_obj.filepath = valid_filepath
        test_obj.download_vid()

        mock_instance.download.assert_called_once_with(valid_url)