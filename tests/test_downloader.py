from helpers import downloader

def test_download_init():
    valid_url = "https://www.youtube.com/watch?v=testtesttes"
    valid_type = "video"
    valid_mode = "single"
    test_obj = downloader.Download(valid_url, valid_type, valid_mode)

    assert test_obj.url == valid_url
    assert test_obj.file_type == valid_type
    assert test_obj.mode == valid_mode