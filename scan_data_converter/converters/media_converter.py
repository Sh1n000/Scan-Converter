from converters.ffmpeg_converter import FFmpegConverter
# from converters.nuke_converter import NukeConverter

import subprocess
from pathlib import Path


class MediaConverter:
    def __init__(self, config: dict):
        self.cfg = config
        self.mode = {
            "exr_to_jpg": self._convert_exr_seq,
            "jpg_seq_to_montage": self._convert_montage,
            "jpg_seq_to_webm": self._convert_webm,
            "jpg_seq_to_mp4": self._convert_mp4,
        }

    def convert(self):
        t = self.cfg.get("type")
        if t not in self.mode:
            raise ValueError(f"Unsupported conversion type: {t}")
        self.mode[t]()

    def _convert_exr_seq(self):
        assert self.cfg["type"] == "exr_to_jpg"
        conv = FFmpegConverter()
        conv.convert(
            input_path=Path(self.cfg["input"]),
            output_path=Path(self.cfg["output"]),
            start_number=self.cfg.get(
                "start_frame", 1001
            ),  # 1001이 아닌 1 프레임부터 출력됨
            options=[],
        )

    def _convert_webm(self):
        conv = FFmpegConverter()
        opts = [
            "-framerate",
            str(self.cfg.get("framerate", 24)),
            "-c:v",
            "libvpx-vp9",
            "-crf",
            "30",
            "-b:v",
            "0",
        ]
        conv.convert(
            input_path=Path(self.cfg["input"]),
            output_path=Path(self.cfg["output"]),
            options=opts,
        )

    def _convert_mp4(self):
        conv = FFmpegConverter()
        opts = [
            "-framerate",
            str(self.cfg.get("framerate", 24)),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
        ]
        conv.convert(
            input_path=Path(self.cfg["input"]),
            output_path=Path(self.cfg["output"]),
            options=opts,
        )

    def _convert_montage(self):
        # ImageMagick montage 사용 예시
        cmd = [
            "montage",
            str(self.cfg["input"]),
            "-tile",
            "5x5",  # 한 행/열에 들어갈 프레임 수
            "-geometry",
            "+2+2",  # 프레임 간 간격
            str(self.cfg["output"]),
        ]
        subprocess.run(cmd, check=True)
