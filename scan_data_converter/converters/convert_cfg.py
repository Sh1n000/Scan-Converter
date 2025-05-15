# managers/convert_config_factory.py

from managers.file_manager import FileManager
from pathlib import Path


class ConvertConfigFactory:
    def __init__(self, file_manager: FileManager):
        self.fm = file_manager
        self.base = Path(self.fm.path)  # 선택된 경로
        self.org_dir = self.base / "org"
        self.jpg_dir = self.base / "jpg"
        self.montage_dir = self.base / "montage"
        self.filmstrip_dir = self.base / "filmstrip"
        # 영상파일들은 폴더 지정 X
        self.webm_dir = self.base
        self.mp4_dir = self.base

    def exr_to_jpg(self) -> dict:
        seqs = self.fm.get_exr_sequences()
        if not seqs:
            raise RuntimeError("EXR 시퀀스를 찾을 수 없습니다.")
        seq = seqs[0]
        head, tail = seq.head(), seq.tail()

        return {
            "input_pattern": str(self.base / f"{head}%07d{tail}"),
            "output_pattern": str(self.jpg_dir / f"{head}%04d.jpg"),
            "start_number": seq.start(),
            "options": [],  # 추가 옵션이 필요하면 여기에
        }

    def jpg_to_webm(self, framerate: int = 24) -> dict:
        """JPG 시퀀스 정보 얻기"""
        jpg_files = sorted((self.base / "jpg").glob("*.jpg"))
        if not jpg_files:
            raise RuntimeError("JPG 시퀀스를 찾을 수 없습니다.")

        # 파일명에서 번호 분리 (e.g. '...0001.jpg' -> 1)
        first = jpg_files[0].stem.split(".")[-1]
        start = int(first)

        """Naming"""
        head = jpg_files[0].stem.rsplit(".", 1)[0]  # 'A206C024_240315_R29Q'
        output_name = "jpg_to_webm"

        return {
            "input_pattern": str(self.jpg_dir / f"{head}.%04d.jpg"),
            "output_pattern": str(self.webm_dir / f"{output_name}.webm"),
            "start_number": start,
            "options": [
                "-framerate",
                str(framerate),
                "-c:v",
                "libvpx-vp9",
                "-crf",
                "30",
                "-b:v",
                "0",
            ],
        }

    def jpg_to_mp4(self, framerate: int = 24) -> dict:
        jpg_files = sorted(self.jpg_dir.glob("*.jpg"))

        if not jpg_files:
            raise RuntimeError("JPG 시퀀스를 찾을 수 없습니다.")
        head, num = jpg_files[0].stem.rsplit(".", 1)
        start = int(num)
        output_name = "jpg_to_mp4"

        return {
            "input_pattern": str(self.jpg_dir / f"{head}.%04d.jpg"),
            "output_pattern": str(self.mp4_dir / f"{output_name}.mp4"),
            "start_number": start,
            "options": [
                "-framerate",
                str(framerate),
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
            ],
        }

    def org_to_mp4(self, framerate: int = 24) -> dict:
        """org 폴더의 EXR 시퀀스를 직접 MP4로 변환"""
        org_fm = FileManager(self.org_dir)
        seqs = org_fm.get_exr_sequences()
        if not seqs:
            raise RuntimeError("org 폴더에서 EXR 시퀀스를 찾을 수 없습니다.")

        # pyseq.Sequence 객체에서 head, tail, start_number 확보
        seq = seqs[0]
        head, tail = (
            seq.head(),
            seq.tail(),
        )  # ex: head="C014C018_240315_R29Q.", tail=".exr"
        start = seq.start()  # ex: 1 or 1001
        output_name = "org_to_mp4"
        return {
            # ex: "/.../org/C014C018_240315_R29Q.%07d.exr"
            "input_pattern": str(self.org_dir / f"{head}%07d{tail}"),
            # 하나의 MP4 파일로 출력
            "output_pattern": str(self.base / f"{output_name}.mp4"),
            "start_number": start,
            "options": [
                "-framerate",
                str(framerate),
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
            ],
        }

    # def jpg_seq_to_tile_montage(
    #     self,
    #     cols: int = 5,
    #     rows: int = 5,
    #     framerate: int = 24,
    #     qscale: int = 2,
    # ) -> dict:
    #     cfg = self.exr_to_jpg()
    #     head = Path(cfg["output_pattern"]).stem.split("%")[0]
    #     return {
    #         "input_pattern": cfg["output_pattern"],
    #         "output_pattern": str(self.montage_dir / f"{head}_montage.jpg"),
    #         "start_number": cfg["start_number"],
    #         "options": [
    #             "-framerate",
    #             str(framerate),
    #             "-filter_complex",
    #             f"tile={cols}x{rows}",
    #             "-qscale:v",
    #             str(qscale),
    #             "-vsync",
    #             "0",
    #         ],
    #     }

    # def jpg_seq_to_filmstrip(
    #     self,
    #     columns: int = 5,
    #     scale: str = None,
    #     framerate: int = 24,
    # ) -> dict:
    #     cfg = self.exr_to_jpg()
    #     head = Path(cfg["output_pattern"]).stem.split("%")[0]
    #     filters = []
    #     if scale:
    #         filters.append(f"scale={scale}")
    #     filters.append(f"tile={columns}x1")
    #     return {
    #         "input_pattern": cfg["output_pattern"],
    #         "output_pattern": str(self.filmstrip_dir / f"{head}_filmstrip.jpg"),
    #         "start_number": None,
    #         "options": [
    #             "-framerate",
    #             str(framerate),
    #             "-filter_complex",
    #             ",".join(filters),
    #             "-frames:v",
    #             "1",
    #         ],
    #     }

    def get(self, mode: str, **kwargs) -> dict:
        mapping = {
            "exr_to_jpg": self.exr_to_jpg,
            "jpg_to_webm": lambda: self.jpg_to_webm(**kwargs),
            "jpg_to_mp4": lambda: self.jpg_to_mp4(**kwargs),
            "org_to_mp4": lambda: self.org_to_mp4(**kwargs),
            # "jpg_seq_to_tile_montage": lambda: self.jpg_seq_to_tile_montage(**kwargs),
            # "jpg_seq_to_filmstrip": lambda: self.jpg_seq_to_filmstrip(**kwargs),
        }
        if mode not in mapping:
            raise ValueError(f"Unknown mode: {mode}")
        return mapping[mode]()
