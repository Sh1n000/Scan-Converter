# converters/media_converter.py
from .ffmpeg_converter import FFmpegConverter
from pathlib import Path
from typing import Union, List, Optional
from typing import Dict
from core.rez_runner import RezRunner


class MediaConverter:
    """
    FFmpegConverter.convert() 하나만 호출하도록 단순화된 MediaConverter.
    config 딕셔너리 키:
      - input_pattern   : str | Path
      - output_pattern  : str | Path
      - start_number    : Optional[int]
      - options         : Optional[List[str]]
    """

    def __init__(self, config: dict):
        self.cfg = config
        self.converter = FFmpegConverter()
        # rez 패키지 리스트: ffmpeg, x264, python-3.9
        self.runner = RezRunner(["ffmpeg", "x264", "python-3.9"])

    # def convert(self):
    #     # config 검증
    #     if "input_pattern" not in self.cfg or "output_pattern" not in self.cfg:
    #         raise ValueError(
    #             "config에 'input_pattern'과 'output_pattern'이 반드시 필요합니다."
    #         )

    #     # 키워드 인자 언패킹
    #     self.converter.convert(
    #         input_pattern=Path(self.cfg["input_pattern"]),
    #         output_pattern=Path(self.cfg["output_pattern"]),
    #         start_number=self.cfg.get("start_number", None),
    #         options=self.cfg.get("options", []),
    #     )
    def convert(self):
        # config 검증
        if "input_pattern" not in self.cfg or "output_pattern" not in self.cfg:
            raise ValueError(
                "config에 'input_pattern'과 'output_pattern'이 반드시 필요합니다."
            )

        # FFmpegConverter.convert 키워드 언패킹
        self.converter.convert(
            input_pattern=Path(self.cfg["input_pattern"]),
            output_pattern=Path(self.cfg["output_pattern"]),
            start_number=self.cfg.get("start_number", None),
            options=self.cfg.get("options", []),
        )
