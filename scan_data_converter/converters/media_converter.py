# media_converter.py

from pathlib import Path
from converters.ffmpeg_converter import FFmpegConverter
# from converters.nuke_converter import NukeConverter


class MediaConverter:
    def __init__(self, config: dict):
        """
        config 예시:
        {
          "type": "exr",          # "exr" 또는 "mov"
          "input": Path(...),
          "output": Path(...),
        }
        """
        self.cfg = config

    def ffmpeg_exr_to_jpg(self):
        # Config 검증
        assert self.cfg["type"] == "exr_seq", "exr_seq 타입이 아닙니다."

        # 입력 패턴과 출력 패턴
        input_pattern = self.cfg["input"]  # e.g. "C014...%07d.exr"
        output_pattern = self.cfg["output"]  # e.g. "/.../jpg/%04d.jpg"
        start_num = self.cfg.get("start_frame", 1001)

        # 1) 컨버터 생성 (no-arg)
        conv = FFmpegConverter()

        # 2) convert() 호출
        conv.convert(
            input_path=Path(input_pattern),
            output_path=Path(output_pattern),
            start_number=start_num,
            options=[],
        )
