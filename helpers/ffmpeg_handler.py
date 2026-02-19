from pathlib import Path
import requests
import shutil
import zipfile


def check_ffmpeg() -> bool:
    """
    Checks if ffmpeg is in PATH

    Returns:
        bool: False if ffmpeg is not detected, True otherwise"""
    if not shutil.which("ffmpeg"):
        return False
    return True


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
    program_dir = Path(__file__).parent.parent
    zip_file = program_dir / "ffmpeg.zip"

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        try:
            with open(zip_file, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
        except (PermissionError, OSError):
            zip_file.unlink()
            raise
    except requests.exceptions.RequestException:
        zip_file.unlink()
        raise

    target_folder = program_dir / "ffmpeg"

    try:
        target_folder.mkdir(exist_ok=True)
    except (PermissionError, OSError):
        zip_file.unlink()
        raise

    try:
        extract_to_target_folder(zip_file, target_folder)
    except (OSError, PermissionError, zipfile.BadZipFile):
        raise


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
