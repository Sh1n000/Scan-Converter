from pathlib import Path
from collections import defaultdict
from typing import Optional
import pyseq


class FileManager:
    """
    1. 파일 확장자 분류
    2. exr 시퀀스 인식
    3. Rename
    """

    def __init__(self, path: Path):
        if not path.exists() or not path.is_dir():
            raise ValueError(f"유효하지 않은 경로: {path}")

        self.path = path
        self.file_dict: dict[str, list[Path]] = defaultdict(list)

    def collect_by_extension(self) -> dict[str, list[Path]]:
        """확장자별로 파일을 분류"""
        for file in self.path.iterdir():
            if file.is_file():
                ext = file.suffix.lower()  # .exr, .mov
                self.file_dict[ext].append(file)

        return self.file_dict

    def get_exr_sequences(self) -> list[pyseq.Sequence]:
        """EXR 파일이 시퀀스로 존재하는 경우 시퀀스로 인식"""
        exr_files = self.file_dict.get(".exr", [])
        if not exr_files:
            return []

        # pyseq.get_sequences 는 str 리스트가 필요함
        seqs = pyseq.get_sequences([str(f) for f in exr_files])
        return seqs
