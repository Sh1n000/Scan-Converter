from converters.ffmpeg_converter import FFmpegConverter
# from converters.nuke_converter import NukeConverter

import subprocess
from pathlib import Path


class MediaConverter:
    def __init__(self, config: dict):
        self.cfg = config
        self.mode = {
            "exr_to_jpg": self._convert_exr_seq,
            "jpg_seq_to_montage": self._convert_tile_montage,
            "jpg_seq_to_webm": self._convert_webm,
            "jpg_seq_to_mp4": self._convert_mp4,
            "jpg_seq_to_filmstrip": self._convert_filmstrip,
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

    # def _convert_tile_montage(self):
    # """ImageMagick Montage Converte"""
    #     assert self.cfg["type"] == "jpg_seq_to_montage"
    #     input_dir = Path(self.cfg["input"])
    #     if not input_dir.is_dir():
    #         raise RuntimeError(f"{input_dir} 가 디렉터리가 아닙니다.")

    #     jpg_files = sorted(input_dir.glob("*.jpg"))
    #     if not jpg_files:
    #         raise RuntimeError(f"No JPG files found in {input_dir}")

    #     output_file = Path(self.cfg["output"])
    #     output_file.parent.mkdir(parents=True, exist_ok=True)

    #     cmd = [
    #         "montage",
    #         *map(str, jpg_files),
    #         "-tile",
    #         self.cfg.get("tile", "5x5"),
    #         "-geometry",
    #         self.cfg.get("geometry", "+2+2"),
    #         str(output_file),
    #     ]
    #     try:
    #         subprocess.run(cmd, check=True)
    #     except FileNotFoundError:
    #         raise RuntimeError(
    #             "'montage' 명령을 찾을 수 없습니다. ImageMagick이 설치되어 있고 PATH에 있는지 확인하세요."
    #         )

    def _convert_tile_montage(self):
        assert self.cfg["type"] == "jpg_seq_to_tile_montage"
        pattern = self.cfg["input_pattern"]  # ex: '…/jpg/exr_to_jpg.%04d.jpg'
        output = self.cfg["output"]
        tile = self.cfg.get("tile", "5x5")
        qscale = self.cfg.get("qscale", 2)
        fr = self.cfg.get("framerate", 25)

        cmd = [
            "ffmpeg",
            "-framerate",
            str(fr),  # 이미지 시퀀스 입력 프레임레이트
            "-i",
            pattern,
            "-filter_complex",
            f"tile={tile}",
            "-qscale:v",
            str(qscale),
            "-vsync",
            "0",  # 프레임 싱크 강제 비활성
            str(output),
        ]

        # stderr/stdout 캡처
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            # 에러 메시지 전체를 출력해 줌
            raise RuntimeError("FFmpeg 몽타주 생성 실패:\n\n" + proc.stderr.strip())

    def _convert_filmstrip(self):
        assert self.cfg["type"] == "jpg_seq_to_filmstrip"
        pattern = self.cfg["input_pattern"]  # ex: '/…/%04d.jpg'
        output = self.cfg["output"]
        cols = self.cfg.get("columns", 10)
        scale = self.cfg.get("scale", None)

        # filter_complex = "scale=320:-1,tile=10x1" 순서대로 적용
        filters = []
        if scale:
            filters.append(f"scale={scale}")
        filters.append(f"tile={cols}x1")
        filter_complex = ",".join(filters)

        cmd = [
            "ffmpeg",
            "-i",
            pattern,
            "-filter_complex",
            filter_complex,
            "-frames:v",
            "5",  # 최종 이미지 한 장만
            str(output),
        ]

        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError("FFmpeg filmstrip 생성 실패:\n" + proc.stderr.strip())
