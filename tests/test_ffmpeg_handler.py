from helpers import ffmpeg_handler
from unittest.mock import patch

def test_dependency_checking():
    with patch("shutil.which", return_value = None):
        assert ffmpeg_handler.check_ffmpeg() == False   