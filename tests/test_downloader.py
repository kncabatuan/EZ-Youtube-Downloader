from helpers import downloader
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