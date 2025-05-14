from managers.file_manager import FileManager


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

    def jpg_seq_to_montage(self) -> dict:
        cfg = self.exr_to_jpg()
        return {
            **cfg,
            "type": "jpg_seq_to_montage",
            "input": cfg["output"],
            "output": str(self.path / "montage" / "jpg_to_montage.%04d.jpg"),
        }

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

    def get(self, mode: str, **kwargs) -> dict:
        """mode 이름으로 해당 메서드를 호출"""
        mapping = {
            "exr_to_jpg": self.exr_to_jpg,
            "jpg_seq_to_montage": self.jpg_seq_to_montage,
            "jpg_seq_to_webm": lambda: self.jpg_seq_to_webm(**kwargs),
            "jpg_seq_to_mp4": lambda: self.jpg_seq_to_mp4(**kwargs),
        }
        if mode not in mapping:
            raise ValueError(f"Unknown mode: {mode}")
        return mapping[mode]()
