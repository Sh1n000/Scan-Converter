# converters/ffmpeg_converter.py
from pathlib import Path
from core.rez_runner import RezRunner
from .base import ConverterBackend


class FFmpegConverter(ConverterBackend):
    """FFmpeg 기반 미디어 변환 백엔드"""

    def __init__(self, rez_pkgs: list[str] = ["ffmpeg"]):
        self.rez = RezRunner(rez_pkgs)

    def convert(self, src: Path, dst: Path) -> bool:
        cmd = ["ffmpeg", "-y", "-i", str(src), str(dst)]
        result = self.rez.run(cmd)
        if result.returncode != 0:
            print(f"[FFmpegConverter] Error:\n{result.stderr}")
            return False
        return True
