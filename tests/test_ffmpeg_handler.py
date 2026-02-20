from helpers import ffmpeg_handler
from unittest.mock import patch, Mock
import pytest
import requests
import shutil
import subprocess

def test_dependency_checking():
    with patch("shutil.which", return_value = None):
        assert ffmpeg_handler.check_ffmpeg() == False


def test_ffmpeg_bin_finding_valid(tmp_path):
    temp_dir = tmp_path / "Temporary Directory"
    temp_dir.mkdir()

    temp_bin_path = temp_dir / "ffmpeg" / "ffmpeg-release-essentials" / "bin"
    temp_bin_path.mkdir(parents=True)

    temp_exe_file = temp_bin_path / "test.exe"
    temp_exe_file.touch()

    with patch("helpers.ffmpeg_handler.PROGRAM_DIR", temp_dir):
        with patch("helpers.ffmpeg_handler.check_ffmpeg_bin_files", return_value = True):
            ffmpeg_bin = ffmpeg_handler.find_ffmpeg_bin()

    assert ffmpeg_bin == temp_bin_path


def test_ffmpeg_bin_finding_invalid(tmp_path):
    temp_dir = tmp_path / "Temporary Directory"
    temp_dir.mkdir()

    temp_invalid_bin_paths = [
        temp_dir / "test",
        temp_dir / "ffmpeg",
        temp_dir / "ffmpeg" / "test",
        temp_dir / "ffmpeg" / "ffmpeg-release-essentials",
        temp_dir / "ffmpeg" / "ffmpeg-release-essentials" / "test",
        temp_dir / "ffmpeg" / "ffmpeg-release-essentials" / "bin"
    ]

    for path in temp_invalid_bin_paths:
        path.mkdir(parents=True)

        with patch("helpers.ffmpeg_handler.PROGRAM_DIR", temp_dir):
            with pytest.raises(FileNotFoundError):
                _ = ffmpeg_handler.find_ffmpeg_bin()
        
        shutil.rmtree(path, ignore_errors=True)


def test_ffmpeg_exe_checking_valid(tmp_path):
    temp_dir = tmp_path / "Temporary Directory"
    temp_dir.mkdir()

    temp_bin_path = temp_dir / "ffmpeg" / "ffmpeg-release-essentials" / "bin"
    temp_bin_path.mkdir(parents=True)

    temp_exe_path = temp_bin_path / "ffmpeg.exe"
    temp_exe_path.touch()

    mock_results = Mock()
    mock_results = subprocess.CompletedProcess(
        args=[str(temp_exe_path), "-version"],
        returncode=0
    )

    with patch("helpers.ffmpeg_handler.subprocess.run", return_value=mock_results):
        assert ffmpeg_handler.check_ffmpeg_bin_files(temp_bin_path) == True


def test_ffmpeg_exe_checking_invalid(tmp_path):
    temp_dir = tmp_path / "Temporary Directory"
    temp_dir.mkdir()

    temp_bin_path = temp_dir / "ffmpeg" / "ffmpeg-release-essentials" / "bin"
    temp_bin_path.mkdir(parents=True)

    with pytest.raises(FileNotFoundError):
        ffmpeg_handler.check_ffmpeg_bin_files(temp_bin_path)

    temp_exe_path = temp_bin_path / "ffmpeg.exe"
    temp_exe_path.touch()

    with patch("helpers.ffmpeg_handler.subprocess.run", side_effect=subprocess.CalledProcessError(
        returncode=1,
        cmd=[str(temp_exe_path), "-version"]
    )):
        
        with pytest.raises(subprocess.CalledProcessError):
            ffmpeg_handler.check_ffmpeg_bin_files(temp_bin_path)


def test_ffmpeg_download(tmp_path):
    test_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    
    temp_dir = tmp_path / "Temporary Directory"
    temp_dir.mkdir()

    test_zip_file = temp_dir / "ffmpeg.zip"
    
    test_target_folder = temp_dir / "ffmpeg"

    with patch("helpers.ffmpeg_handler.PROGRAM_DIR", temp_dir):
        with (
            patch("helpers.ffmpeg_handler.get_ffmpeg_zip_from_url") as mock_get,
            patch("helpers.ffmpeg_handler.make_target_folder") as mock_make,
            patch("helpers.ffmpeg_handler.extract_to_target_folder") as mock_extract
        ):
            ffmpeg_handler.download_ffmpeg()

            mock_get.assert_called_once_with(test_url, test_zip_file)
            mock_make.assert_called_once_with(test_target_folder)
            mock_extract.assert_called_once_with(test_zip_file, test_target_folder)


def test_ffmpeg_download_raise(tmp_path):
    test_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    
    temp_dir = tmp_path / "Temporary Directory"
    temp_dir.mkdir()

    test_zip_file = temp_dir / "ffmpeg.zip"

    exceptions_1 = [OSError, PermissionError, requests.exceptions.RequestException]
    for exception in exceptions_1:
        with patch("helpers.ffmpeg_handler.PROGRAM_DIR", temp_dir):
            with patch("helpers.ffmpeg_handler.get_ffmpeg_zip_from_url", side_effect=exception):
                with pytest.raises(exception):
                    ffmpeg_handler.download_ffmpeg()