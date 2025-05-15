# converters/ffmpeg_converter.py
from typing import Optional
from .base import ConverterBackend
from pathlib import Path
import subprocess


class FFmpegConverter(ConverterBackend):
    def convert(
        self,
        input_pattern: Path,
        output_pattern: Path,
        start_number: Optional[int] = None,
        options: Optional[list[str]] = None,
    ):
        """
        범용 FFmpeg 변환 메서드.
        - input_pattern: 프레임 시퀀스/단일 파일 패턴
        - output_pattern: 출력 파일 패턴
        - start_number: 시퀀스 시작 번호 (없어도 됨)
        - options: ffmpeg 추가 옵션 리스트
        """
        cmd: list[str] = ["ffmpeg"]

        if start_number is not None:
            cmd += ["-start_number", str(start_number)]

        cmd += ["-i", str(input_pattern)]
        if options:
            cmd += options

        cmd += [str(output_pattern)]
        subprocess.run(cmd, check=True)
