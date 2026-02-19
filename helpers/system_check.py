from pathlib import Path
import requests
import shutil
import zipfile

def check_dependency() -> bool:
    if not shutil.which("ffmpeg"):
        return False
    return True


def download_ffmpeg() -> None:
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    file = "ffmpeg-release-essentials.zip"

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(file, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    except requests.exceptions.RequestException:
        return
    
    program_dir = Path(__file__).parent.parent
    zip_file = program_dir / file
    target_folder = program_dir / "ffmpeg"

    try:
        target_folder.mkdir(exist_ok=True)
    except (PermissionError, OSError):
        return
    
    extract_to_target_folder(zip_file, target_folder)
    

def extract_to_target_folder(downloaded_zip: Path, folder_path: Path) -> None:
    shutil.move(downloaded_zip, folder_path / downloaded_zip.name)

    with zipfile.ZipFile(downloaded_zip, "r") as zip_ref:
        zip_ref.extractall(folder_path)
                           
    downloaded_zip.unlink()