from .base import ConverterBackend
from pathlib import Path
import subprocess


class FFmpegConverter(ConverterBackend):
    def convert(self, input_path: Path, output_path: Path, **kwargs):
        cmd = [
            "ffmpeg",
            "-start_number",
            str(kwargs.get("start_number", 1001)),
            "-i",
            str(input_path),
            *kwargs.get("options", []),
            str(output_path),
        ]
        subprocess.run(cmd, check=True)
