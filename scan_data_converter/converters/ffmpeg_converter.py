# converters/ffmpeg_converter.py
from .base import ConverterBackend
from pathlib import Path
import subprocess


class FFmpegConverter(ConverterBackend):
    def convert(
        self, input_path: Path, output_path: Path, mode: str = "exr_to_jpg", **kwargs
    ):
        """
        mode: "exr_to_jpg", "jpg_to_montage", "jpg_to_mp4", "jpg_to_webm" 중 하나.
        """
        if mode == "exr_to_jpg":
            return self.exr_to_jpg(input_path, output_path, **kwargs)
        elif mode == "jpg_to_montage":
            return self.jpg_to_montage(input_path, output_path, **kwargs)
        elif mode == "jpg_to_mp4":
            return self.jpg_to_mp4(input_path, output_path, **kwargs)
        elif mode == "jpg_to_webm":
            return self.jpg_to_webm(input_path, output_path, **kwargs)
        else:
            raise ValueError(f"Unknown mode: {mode}")

    def exr_to_jpg(
        self,
        input_pattern: Path,
        output_pattern: Path,
        start_number: int = 1001,
        **kwargs,  # ← here
    ):
        options = kwargs.get("options", [])  # 전달된 옵션 가져오기
        cmd = [
            "ffmpeg",
            "-start_number",
            str(start_number),
            "-i",
            str(input_pattern),
            *options,  # 옵션 추가
            str(output_pattern),
        ]
        subprocess.run(cmd, check=True)

    def jpg_to_montage(
        self,
        input_pattern: Path,
        output_path: Path,
        cols: int = 5,
        rows: int = 5,
        start_number: int = 1,
    ):
        cmd = [
            "ffmpeg",
            "-start_number",
            str(start_number),
            "-i",
            str(input_pattern),
            "-vf",
            f"tile={cols}x{rows}",
            str(output_path),
        ]
        subprocess.run(cmd, check=True)

    def jpg_to_mp4(self, input_pattern: Path, output_path: Path, framerate: int = 24):
        cmd = [
            "ffmpeg",
            "-framerate",
            str(framerate),
            "-i",
            str(input_pattern),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            str(output_path),
        ]
        subprocess.run(cmd, check=True)

    def jpg_to_webm(
        self, input_pattern: Path, output_path: Path, framerate: int = 24, crf: int = 30
    ):
        cmd = [
            "ffmpeg",
            "-framerate",
            str(framerate),
            "-i",
            str(input_pattern),
            "-c:v",
            "libvpx-vp9",
            "-b:v",
            "0",
            "-crf",
            str(crf),
            str(output_path),
        ]
        subprocess.run(cmd, check=True)
