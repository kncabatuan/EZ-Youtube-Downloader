from pathlib import Path
import os
import requests
import shutil
import subprocess
import sys
import zipfile

# The root program directory
if getattr(sys, "frozen", False):
    # Running as a frozen exe
    local_app_data = os.getenv("LOCALAPPDATA")
    assert local_app_data is not None
    APPDATA_DIR = Path(local_app_data) / "EZYoutube"
    APPDATA_DIR.mkdir(parents=True, exist_ok=True)
else:
    # Running normally from source
    APPDATA_DIR = Path(__file__).parent.parent


def check_ffmpeg() -> bool:
    """
    Checks if ffmpeg is in PATH

    Returns:
        bool: False if ffmpeg is not detected, True otherwise
    """
    if not shutil.which("ffmpeg"):
        return False
    return True


def find_ffmpeg_bin() -> Path:
    """
    Checks program directory if a bin folder for ffmpeg exists

    Calls function to check ffmpeg.exe integrity

    Returns:
        Path: The file path of the bin folder that contains ffmpeg.exe

    Raises:
        FileNotFoundError: If relevant folder/files were not detected
        PermissionError: If the user does not have permission to access program directory
        OSError: If other os-related error occurs
        subprocess.CalledProcessError: If running of ffmpeg.exe fails
    """
    ffmpeg_dir = APPDATA_DIR / "ffmpeg"
    ffmpeg_bin = None

    if ffmpeg_dir.exists() and any(ffmpeg_dir.iterdir()):
        for item in ffmpeg_dir.iterdir():
            if (
                item.is_dir()
                and "essentials" in item.name.lower()
                and any(item.iterdir())
            ):
                for sub_item in item.iterdir():
                    if sub_item.name == "bin" and any(sub_item.iterdir()):
                        ffmpeg_bin = sub_item
                        break
                break
        if ffmpeg_bin is None:
            raise FileNotFoundError
    else:
        raise FileNotFoundError

    try:
        check_ffmpeg_bin_files(ffmpeg_bin)
        return ffmpeg_bin
    except Exception:
        raise


def check_ffmpeg_bin_files(ffmpeg_bin: Path) -> bool:
    """
    Handles checking of ffmpeg.exe integrity

    Args:
        ffmpeg_bin (Path): Filepath of the bin folder that contains ffmpeg.exe

    Returns:
        bool: True if ffmpeg.exe is detected and ran properly

    Raises:
        FileNotFoundError: If relevant folder/files were not detected
        PermissionError: If the user does not have permission to access program directory
        OSError: If other os-related error occurs
        subprocess.CalledProcessError: If running of ffmpeg.exe fails
    """
    ffmpeg_exe_path = ffmpeg_bin / "ffmpeg.exe"
    if ffmpeg_exe_path.exists():
        try:
            _ = subprocess.run(
                [str(ffmpeg_exe_path), "-version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            return True
        except (PermissionError, OSError, subprocess.CalledProcessError):
            raise
    else:
        raise FileNotFoundError


def download_ffmpeg() -> None:
    """
    Handles downloading of ffmpeg zip file

    Removes residual files if download is interrupted or file is corrupted

    Raises:
        PermissionError: If user does not have permission to access program files
        OSError: If other os-related error occurs
        requests.exceptions.RequestException: If any exception from the requests library occurs
        zipfile.BadZipFile: If the downloaded zip file is corrupted or incomplete
    """
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_file = APPDATA_DIR / "ffmpeg.zip"

    if zip_file.exists():
        zip_file.unlink()

    try:
        get_ffmpeg_zip_from_url(url, zip_file)
    except (PermissionError, OSError, requests.exceptions.RequestException):
        if zip_file.exists():
            zip_file.unlink()
        raise

    target_folder = APPDATA_DIR / "ffmpeg"

    try:
        make_target_folder(target_folder)
    except (PermissionError, OSError):
        if zip_file.exists():
            zip_file.unlink()
        raise

    try:
        extract_to_target_folder(zip_file, target_folder)
    except (OSError, PermissionError, zipfile.BadZipFile):
        raise


def get_ffmpeg_zip_from_url(url: str, zip_file: Path) -> None:
    """
    Gets the ffmpeg zip file from ffmpeg site

    Args:
        url (str): ffmpeg url
        zip_file (Path): The path of the zip file that will be created from downloading

    Raises:
        PermissionError: If the user does not have permission to create a file in the program directory
        OSError: If other os-related error occurs
        requests.exceptions.RequestException: If an error from requests occurs
    """

    response = requests.get(url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get("Content-Length", 0))
    block_size = 8192  # 8 kb
    downloaded = 0
    try:
        with open(zip_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=block_size):
                f.write(chunk)
                downloaded += len(chunk)
                percent_done = (downloaded / total_size) * 100
                print(f"\rDownloading ffmpeg: {percent_done:.2f}%", flush=True, end="")
    except (PermissionError, OSError):
        raise


def make_target_folder(target_folder: Path) -> None:
    """
    Creates the target folder for extraction of the ffmpeg zip file

    Args:
        target_folder (Path): The path of the target folder

    Raises:
        PermissionError: If user does not have permission to create a folder in program directory
        OSError: If other os-related error occurs
    """

    if target_folder.exists():
        shutil.rmtree(target_folder, ignore_errors=True)
    target_folder.mkdir()


def extract_to_target_folder(downloaded_zip: Path, folder_path: Path) -> None:
    """
    Moves the downloaded zipfile to the proper directory, extracts it, then deletes it

    Removes the ffmpeg directory in program files if extraction fails

    Args:
        downloaded_zip (Path): The path to the downloaded zip file
        folder_path: The path where the downloaded zip file should be moved

    Raises:
        PermissionError: If user does not have permission to access program files
        OSError: If other os-related error occurs
        zipfile.BadZipFile: If the downloaded zip file is corrupted or incomplete
    """
    target_zip = folder_path / downloaded_zip.name
    if target_zip.exists():
        target_zip.unlink()

    shutil.move(downloaded_zip, target_zip)

    try:
        with zipfile.ZipFile(target_zip, "r") as zip_ref:
            zip_ref.extractall(folder_path)
    except zipfile.BadZipFile:
        shutil.rmtree(folder_path, ignore_errors=True)
        raise

    target_zip.unlink()
