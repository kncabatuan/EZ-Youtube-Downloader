from helpers import ffmpeg_handler
from unittest.mock import patch, Mock, MagicMock
import pytest
import requests
import shutil
import subprocess
import zipfile


def test_dependency_checking():
    """Tests the checking of ffmpeg in the PATH"""
    with patch("shutil.which", return_value=None):
        assert ffmpeg_handler.check_ffmpeg() == False


def test_ffmpeg_bin_finding_valid(tmp_path):
    """Tests the behavior of find_ffmpeg_bin function when the bin exists and is valid"""
    temp_dir = tmp_path / "Temporary Directory"
    temp_dir.mkdir()

    temp_bin_path = temp_dir / "ffmpeg" / "ffmpeg-release-essentials" / "bin"
    temp_bin_path.mkdir(parents=True)

    temp_exe_file = temp_bin_path / "test.exe"
    temp_exe_file.touch()

    with patch("helpers.ffmpeg_handler.APPDATA_DIR", temp_dir):
        with patch("helpers.ffmpeg_handler.check_ffmpeg_bin_files", return_value=True):
            ffmpeg_bin = ffmpeg_handler.find_ffmpeg_bin()

    assert ffmpeg_bin == temp_bin_path


def test_ffmpeg_bin_finding_invalid(tmp_path):
    """Tests the behavior of find_ffmpeg_bin function when the bin is invalid or non-existent"""
    temp_dir = tmp_path / "Temporary Directory"
    temp_dir.mkdir()

    temp_invalid_bin_paths = [
        temp_dir / "test",
        temp_dir / "ffmpeg",
        temp_dir / "ffmpeg" / "test",
        temp_dir / "ffmpeg" / "ffmpeg-release-essentials",
        temp_dir / "ffmpeg" / "ffmpeg-release-essentials" / "test",
        temp_dir / "ffmpeg" / "ffmpeg-release-essentials" / "bin",
    ]

    for path in temp_invalid_bin_paths:
        path.mkdir(parents=True)

        with patch("helpers.ffmpeg_handler.APPDATA_DIR", temp_dir):
            with pytest.raises(FileNotFoundError):
                _ = ffmpeg_handler.find_ffmpeg_bin()

        shutil.rmtree(path, ignore_errors=True)


def test_ffmpeg_exe_checking_valid(tmp_path):
    """Tests the behavior of check_ffmpeg_bin_files function if ffmpeg.exe is valid, existent, complete, and not corrupt"""
    temp_dir = tmp_path / "Temporary Directory"
    temp_dir.mkdir()

    temp_bin_path = temp_dir / "ffmpeg" / "ffmpeg-release-essentials" / "bin"
    temp_bin_path.mkdir(parents=True)

    temp_exe_path = temp_bin_path / "ffmpeg.exe"
    temp_exe_path.touch()

    mock_results = Mock()
    mock_results = subprocess.CompletedProcess(
        args=[str(temp_exe_path), "-version"], returncode=0
    )

    with patch("helpers.ffmpeg_handler.subprocess.run", return_value=mock_results):
        assert ffmpeg_handler.check_ffmpeg_bin_files(temp_bin_path) == True


def test_ffmpeg_exe_checking_invalid(tmp_path):
    """Tests the behavior of check_ffmpeg_bin_files function if ffmpeg.exe is invalid, does not exist, incomplete or corrupt"""
    temp_dir = tmp_path / "Temporary Directory"
    temp_dir.mkdir()

    temp_bin_path = temp_dir / "ffmpeg" / "ffmpeg-release-essentials" / "bin"
    temp_bin_path.mkdir(parents=True)

    with pytest.raises(FileNotFoundError):
        ffmpeg_handler.check_ffmpeg_bin_files(temp_bin_path)

    temp_exe_path = temp_bin_path / "ffmpeg.exe"
    temp_exe_path.touch()

    with patch(
        "helpers.ffmpeg_handler.subprocess.run",
        side_effect=subprocess.CalledProcessError(
            returncode=1, cmd=[str(temp_exe_path), "-version"]
        ),
    ):

        with pytest.raises(subprocess.CalledProcessError):
            ffmpeg_handler.check_ffmpeg_bin_files(temp_bin_path)


def test_ffmpeg_download_helper_behavior(tmp_path):
    """Tests the behavior of download_ffmpeg function if all helper functions worked properly"""
    test_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

    temp_dir = tmp_path / "Temporary Directory"
    temp_dir.mkdir()

    test_zip_file = temp_dir / "ffmpeg.zip"

    test_target_folder = temp_dir / "ffmpeg"

    with patch("helpers.ffmpeg_handler.APPDATA_DIR", temp_dir):
        with (
            patch("helpers.ffmpeg_handler.get_ffmpeg_zip_from_url") as mock_get,
            patch("helpers.ffmpeg_handler.make_target_folder") as mock_make,
            patch("helpers.ffmpeg_handler.extract_to_target_folder") as mock_extract,
        ):
            ffmpeg_handler.download_ffmpeg()

            mock_get.assert_called_once_with(test_url, test_zip_file)
            mock_make.assert_called_once_with(test_target_folder)
            mock_extract.assert_called_once_with(test_zip_file, test_target_folder)


def test_ffmpeg_download_raising_1(tmp_path):
    """Tests behavior of ffmpeg_download function if get_ffmpeg_zip_from_url fails"""
    temp_dir = tmp_path / "Temporary Directory"
    temp_dir.mkdir()

    exceptions = [OSError, PermissionError, requests.exceptions.RequestException]
    for exception in exceptions:
        test_zip_file = temp_dir / "ffmpeg.zip"
        test_zip_file.touch()

        with patch("helpers.ffmpeg_handler.APPDATA_DIR", temp_dir):
            with patch(
                "helpers.ffmpeg_handler.get_ffmpeg_zip_from_url", side_effect=exception
            ):
                with pytest.raises(exception):
                    ffmpeg_handler.download_ffmpeg()

                assert not test_zip_file.exists()


def test_ffmpeg_download_raising_2(tmp_path):
    """Tests behavior of ffmpeg_download function if make_target_folder fails"""
    temp_dir = tmp_path / "Temporary Directory"
    temp_dir.mkdir()

    exceptions = [OSError, PermissionError]
    for exception in exceptions:
        test_zip_file = temp_dir / "ffmpeg.zip"
        test_zip_file.touch()

        with patch("helpers.ffmpeg_handler.APPDATA_DIR", temp_dir):
            with patch(
                "helpers.ffmpeg_handler.get_ffmpeg_zip_from_url", return_value=None
            ):
                with patch(
                    "helpers.ffmpeg_handler.make_target_folder", side_effect=exception
                ):
                    with pytest.raises(exception):
                        ffmpeg_handler.download_ffmpeg()

                    assert not test_zip_file.exists()


def test_ffmpeg_download_raising_3(tmp_path):
    """Tests behavior of ffmpeg_download function if extract_to_target_folder fails"""
    temp_dir = tmp_path / "Temporary Directory"
    temp_dir.mkdir()

    test_zip_file = temp_dir / "ffmpeg.zip"
    test_zip_file.touch()

    exceptions = [OSError, PermissionError, zipfile.BadZipFile]
    for exception in exceptions:
        with patch("helpers.ffmpeg_handler.APPDATA_DIR", temp_dir):
            with patch(
                "helpers.ffmpeg_handler.get_ffmpeg_zip_from_url", return_value=None
            ):
                test_target_folder = temp_dir / "ffmpeg"

                with patch(
                    "helpers.ffmpeg_handler.make_target_folder", return_value=None
                ):
                    test_target_folder.mkdir(exist_ok=True)

                    with patch(
                        "helpers.ffmpeg_handler.extract_to_target_folder",
                        side_effect=exception,
                    ):
                        with pytest.raises(exception):
                            ffmpeg_handler.download_ffmpeg()


def test_get_zip_from_url_success(tmp_path):
    """Tests get_zip_from_url function behavior if requests.get and writing the downloaded file is successful"""
    test_zip_file = tmp_path / "ffmpeg.zip"
    test_url = "https://www.test_url.com"

    fake_content = [b"test", b"contents"]

    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.iter_content.return_value = fake_content
    mock_response.headers = {"Content-Length": "8"}

    with patch(
        "helpers.ffmpeg_handler.requests.get", return_value=mock_response
    ) as mock_get:
        ffmpeg_handler.get_ffmpeg_zip_from_url(test_url, test_zip_file)

    mock_get.assert_called_once_with(test_url, stream=True, timeout=10)
    assert test_zip_file.exists()
    assert test_zip_file.read_bytes() == b"testcontents"


def test_get_zip_from_url_fail(tmp_path):
    """Tests get_zip_from_url function behavior if requests.get or writing the downloaded file fails"""
    test_zip_file = tmp_path / "ffmpeg.zip"
    test_url = "https://www.test_url.com"

    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.RequestException
    mock_response.headers = {"Content-Length": "8"}

    with patch("helpers.ffmpeg_handler.requests.get", return_value=mock_response):
        with pytest.raises(requests.exceptions.RequestException):
            ffmpeg_handler.get_ffmpeg_zip_from_url(test_url, test_zip_file)

    assert not test_zip_file.exists()

    mock_response.raise_for_status.side_effect = None
    mock_response.raise_for_status.return_value = None

    exceptions = [OSError, PermissionError]
    for exception in exceptions:
        with patch("helpers.ffmpeg_handler.requests.get", return_value=mock_response):
            with patch("builtins.open", side_effect=exception):
                with pytest.raises(exception):
                    ffmpeg_handler.get_ffmpeg_zip_from_url(test_url, test_zip_file)

                assert not test_zip_file.exists()


def test_extract_to_target_folder_success(tmp_path):
    """Tests extract_to_target_folder if movement of zip_file and extraction succeeds"""
    temp_dir = tmp_path / "temp_dir"
    temp_dir.mkdir()

    test_zip_file = temp_dir / "test_zip_file.zip"
    test_zip_file.touch()

    test_target_folder = temp_dir / "test_target_folder"
    test_target_folder.mkdir(exist_ok=True)

    mock_zip = MagicMock()
    mock_zip.__enter__.return_value = mock_zip
    mock_zip.__exit__.return_value = None

    fake_extracted_file = test_target_folder / "fake_file.exe"

    mock_zip.extractall.side_effect = lambda _: fake_extracted_file.touch()

    with patch(
        "helpers.ffmpeg_handler.zipfile.ZipFile", return_value=mock_zip
    ) as mock_zip_file:
        ffmpeg_handler.extract_to_target_folder(test_zip_file, test_target_folder)

        test_target_zip = test_target_folder / test_zip_file.name

        mock_zip_file.assert_called_once_with(test_target_zip, "r")
        mock_zip.extractall.assert_called_once_with(test_target_folder)

        assert not test_zip_file.exists()
        assert not (test_target_folder / test_zip_file.name).exists()
        assert fake_extracted_file.exists()


def test_extract_to_target_folder_fail(tmp_path):
    """Tests extract_to_target_folder if movement of zip_file or extraction fails"""
    temp_dir = tmp_path / "temp_dir"
    temp_dir.mkdir()

    test_zip_file = temp_dir / "test_zip_file.zip"
    test_zip_file.touch()

    test_target_folder = temp_dir / "test_target_folder"
    test_target_folder.mkdir(exist_ok=True)

    exceptions = [PermissionError, OSError]
    for exception in exceptions:
        with patch("helpers.ffmpeg_handler.shutil.move", side_effect=exception):
            with pytest.raises(exception):
                ffmpeg_handler.extract_to_target_folder(
                    test_zip_file, test_target_folder
                )

    with patch(
        "helpers.ffmpeg_handler.zipfile.ZipFile", side_effect=zipfile.BadZipFile
    ):
        with pytest.raises(zipfile.BadZipFile):
            ffmpeg_handler.extract_to_target_folder(test_zip_file, test_target_folder)

        assert not test_target_folder.exists()
