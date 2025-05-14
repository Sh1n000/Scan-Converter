from managers.file_manager import FileManager
from pathlib import Path


class ConvertConfigFactory:
    def __init__(self, file_manager: FileManager):
        """
        FFmpeg Convert Config Factory
        1. exr to jpg
        2. jpg to montage
        3. jpg to webm
        4. jpg to mp4 <- Rez 사용 예정
        """
        self.fm = file_manager
        self.path = file_manager.path

    def exr_to_jpg(self) -> dict:
        seqs = self.fm.get_exr_sequences()
        if not seqs:
            raise RuntimeError("EXR 시퀀스를 찾을 수 없습니다.")
        seq = seqs[0]
        head, tail = seq.head(), seq.tail()
        pattern = f"{head}%07d{tail}"
        return {
            "type": "exr_to_jpg",
            "input": str(self.path / pattern),
            "output": str(self.path / "jpg" / "exr_to_jpg.%04d.jpg"),
            "start_frame": seq.start(),
        }

    def jpg_seq_to_tile_montage(self) -> dict:
        exr_cfg = self.exr_to_jpg()
        pattern = exr_cfg["output"]  # "/…/jpg/exr_to_jpg.%04d.jpg"
        return {
            "type": "jpg_seq_to_tile_montage",
            # FFmpeg -i 에 줄 시퀀스 패턴
            "input_pattern": pattern,
            "output": str(self.path / "montage" / "jpg_to_tile_montage.jpg"),
            "tile": "5x5",
            "qscale": 2,
            # "start_frame": exr_cfg.get("start_frame", 1),
        }

    # def jpg_seq_to_tile_montage(self) -> dict:
    #     """IMageMagick montage"""
    #     exr_cfg = self.exr_to_jpg()
    #     jpg_dir = Path(exr_cfg["output"]).parent

    #     return {
    #         "type": "jpg_seq_to_montage",
    #         "input": str(jpg_dir),
    #         "output": str(self.path / "montage" / "jpg_to_tile_montage.jpg"),
    #         "tile": "5x5",
    #         "geometry": "+2+2",
    #     }

    def jpg_seq_to_webm(self, framerate: int = 24) -> dict:
        cfg = self.exr_to_jpg()
        return {
            **cfg,
            "type": "jpg_seq_to_webm",
            "input": cfg["output"],
            "output": str(self.path / "jpg_to_webm.%04d.webm"),
            "framerate": framerate,
        }

    def jpg_seq_to_mp4(self, framerate: int = 24) -> dict:
        cfg = self.exr_to_jpg()
        return {
            **cfg,
            "type": "jpg_seq_to_mp4",
            "input": cfg["output"],
            "output": str(self.path / "jpg_to_mp4.%04d.mp4"),
            "framerate": framerate,
        }

    def jpg_seq_to_filmstrip(self, columns: int = 5) -> dict:
        # 1) EXR→JPG 설정 가져오기
        exr_cfg = self.exr_to_jpg()
        return {
            "type": "jpg_seq_to_filmstrip",
            # FFmpeg -i 에 넘길 시퀀스 패턴 (e.g. “…/%04d.jpg”)
            "input_pattern": exr_cfg["output"],
            # 결과물 경로
            "output": str(self.path / "filmstrip" / f"filmstrip_{columns}x1.jpg"),
            # 한 줄에 넣을 프레임 개수
            "columns": columns,
            # 필요 시 리사이즈
            "scale": None,
        }

    def get(self, mode: str, **kwargs) -> dict:
        """mode 이름으로 해당 메서드를 호출"""
        mapping = {
            "exr_to_jpg": self.exr_to_jpg,
            "jpg_seq_to_tile_montage": self.jpg_seq_to_tile_montage,
            "jpg_seq_to_filmstrip": lambda: self.jpg_seq_to_filmstrip(**kwargs),
            "jpg_seq_to_webm": lambda: self.jpg_seq_to_webm(**kwargs),
            "jpg_seq_to_mp4": lambda: self.jpg_seq_to_mp4(**kwargs),
        }
        if mode not in mapping:
            raise ValueError(f"Unknown mode: {mode}")
        return mapping[mode]()
