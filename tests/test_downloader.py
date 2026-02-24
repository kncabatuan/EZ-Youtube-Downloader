from helpers import downloader
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest


# Tests initialization of the Download class
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


# Tests the extraction of the url based on the mode of download
def test_url_extraction():
    valid_url = "https://www.youtube.com/watch?v=testtesttes&list=test&index=test"
    valid_type = "video"
    modes = ("single", "batch", "playlist")

    test_obj = downloader.Download(valid_url, valid_type, modes[0])
    assert test_obj.url == "https://www.youtube.com/watch?v=testtesttes"

    test_obj = downloader.Download(valid_url, valid_type, modes[1])
    assert test_obj.url == "https://www.youtube.com/watch?v=testtesttes"

    test_obj = downloader.Download(valid_url, valid_type, modes[2])
    assert (
        test_obj.url
        == "https://www.youtube.com/watch?v=testtesttes&list=test&index=test"
    )


# Tests the building of the options dictionary to pass into YoutubeDL
def test_opts_builder():
    valid_url = "https://www.youtube.com/watch?v=testtesttes&list=test&index=test"
    valid_types = ("video", "audio")
    mode = "single"
    filepath = Path("test_filepath")

    test_obj1 = downloader.Download(valid_url, valid_types[0], mode)
    test_obj1.filepath = filepath
    test_obj1.ffmpeg_location = None
    opts1 = test_obj1.opts_builder(use_extractor_args=False, for_title_only=False)

    assert opts1["quiet"] == True
    assert opts1["no_warnings"] == True
    assert opts1["windowsfilenames"] == True
    assert isinstance(opts1["logger"], downloader.MyLogger)
    assert opts1["noplaylist"] == True
    assert opts1["format"] == "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
    assert opts1["merge_output_format"] == "mp4"
    assert opts1["outtmpl"] == str(test_obj1.filepath / "%(title)s.%(ext)s")

    mode = "batch"
    test_obj2 = downloader.Download(valid_url, valid_types[1], mode)
    test_obj2.filepath = filepath
    test_obj2.ffmpeg_location = None
    opts2 = test_obj2.opts_builder(use_extractor_args=True, for_title_only=False)

    assert opts2["extractor_args"] == {
        "youtube": {"player_client": ["android", "mweb", "tv", "ios"]}
    }
    assert opts2["quiet"] == True
    assert opts2["no_warnings"] == True
    assert opts2["windowsfilenames"] == True
    assert isinstance(opts2["logger"], downloader.MyLogger)
    assert opts2["noplaylist"] == True
    assert opts2["format"] == "bestaudio[abr>128]/bestaudio/best"
    assert opts2["outtmpl"] == str(test_obj2.filepath / "%(title)s.%(ext)s")
    assert opts2["postprocessors"] == [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ]


# Tests the extraction of data by YoutubeDL using a valid youtube video URL
def test_data_extraction():
    valid_url = "https://www.youtube.com/watch?v=testtesttes"
    valid_type = "video"
    valid_mode = "single"

    with patch("helpers.downloader.yt_dlp.YoutubeDL") as mock_ydl:
        mock_instance = MagicMock()
        mock_ydl.return_value = mock_instance

        mock_instance.extract_info.return_value = {"title": "Test Title"}

        test_obj = downloader.Download(valid_url, valid_type, valid_mode)
        test_obj.set_title()

        mock_instance.extract_info.assert_called_once_with(
            valid_url, download=False, process=False
        )
        assert test_obj.title == "Test Title"


# Tests the actual downloading using YoutubeDL
def test_download():
    valid_url = "https://www.youtube.com/watch?v=testtesttes"
    valid_type = "video"
    valid_mode = "single"
    valid_filepath = Path("test_filepath")

    with patch("helpers.downloader.yt_dlp.YoutubeDL") as mock_ydl:
        mock_instance = MagicMock()
        mock_ydl.return_value = mock_instance

        test_obj = downloader.Download(valid_url, valid_type, valid_mode)
        test_obj.filepath = valid_filepath
        test_obj.ffmpeg_location = None
        test_obj.download_vid()

        mock_instance.download.assert_called_once_with(valid_url)


# Tests the printing of progress hook
def test_hook_printing(capsys):
    test_total_bytes = 100
    test_downloaded_bytes = 50
    test_filename = "test_title"
    d = {
        "status": "downloading",
        "filename": test_filename,
        "total_bytes": test_total_bytes,
        "downloaded_bytes": test_downloaded_bytes,
    }
    downloader.my_hook(d)

    captured = capsys.readouterr()
    assert captured.out == f"\r\x1b[KDownloading test_title: 50.00%"
