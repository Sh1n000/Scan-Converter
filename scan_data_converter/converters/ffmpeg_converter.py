# converters/ffmpeg_converter.py
from typing import Optional
from .base import ConverterBackend
from pathlib import Path
import subprocess


class FFmpegConverter(ConverterBackend):
    def convert(
        self, input_path: Path, output_path: Path, mode: str = "exr_to_jpg", **kwargs
    ):
        """
        mode: "exr_to_jpg", "jpg_to_tile_montage", "jpg_to_filmstrip", "jpg_to_mp4", "jpg_to_webm"
        """
        if mode == "exr_to_jpg":
            return self.exr_to_jpg(input_path, output_path, **kwargs)
        elif mode == "jpg_to_tile_montage":
            return self.jpg_to_tile_montage(input_path, output_path, **kwargs)
        elif mode == "jpg_to_filmstrip":
            return self.jpg_to_filmstrip(input_path, output_path, **kwargs)
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
        **kwargs,
    ):
        options = kwargs.get("options", [])
        cmd = [
            "ffmpeg",
            "-start_number",
            str(start_number),
            "-i",
            str(input_pattern),
            *options,
            str(output_pattern),
        ]
        subprocess.run(cmd, check=True)

    def jpg_to_tile_montage(
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

    def jpg_to_filmstrip(
        self,
        input_pattern: Path,
        output_path: Path,
        cols: int = 5,
        scale: Optional[str] = None,
        framerate: int = 24,
    ):
        # filmstrip: 한 줄로 cols 장을 나열
        # 1) scale 필터 (선택)
        # 2) tile 필터로 cols × 1 타일 생성
        filters: list[str] = []
        if scale:
            filters.append(f"scale={scale}")
        filters.append(f"tile={cols}x1")
        filter_complex = ",".join(filters)

        cmd = [
            "ffmpeg",
            "-framerate",
            str(framerate),
            "-i",
            str(input_pattern),
            "-filter_complex",
            filter_complex,
            "-frames:v",
            "1",
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
        self,
        input_pattern: Path,
        output_path: Path,
        framerate: int = 24,
        crf: int = 30,
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
