# converters/mp4_converter.py

from core.rez_runner import RezRunner
from pathlib import Path
from typing import Dict


class MP4Converter:
    """
    x264가 포함된 rez-env 안에서
    scripts/convert_to_mp4.py를 실행합니다.
    """

    def __init__(self, config: Dict):
        self.cfg = config
        # 실제 설치된 Rez 패키지 명 확인 후 수정하세요
        self.runner = RezRunner(["ffmpeg", "x264", "python-3.9"])

    def convert(self):
        # 스크립트 경로
        script = Path(__file__).parents[1] / "scripts" / "convert_to_mp4.py"
        cmd = [
            "python",
            str(script),
            "--input",
            self.cfg["input_pattern"],
            "--output",
            self.cfg["output_pattern"],
            "--start",
            str(self.cfg.get("start_number", 1)),
            "--framerate",
            str(
                self.cfg.get("options", ["24"])[1]
            ),  # options에서 프레임레이트 추출 또는 직접 cfg에 저장
        ]
        print("Running in rez-env:", cmd)
        self.runner.run(cmd)
