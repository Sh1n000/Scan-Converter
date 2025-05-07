# from pathlib import Path
# import pyseq


# class FileManager:
#     """
#     경로를 받아서 파일 Type 분석 후
#     이동 및 파일명 변경
#     """

#     def __init__(self, scan_path: Path):
#         self.scan_path = Path(scan_path)

#     def is_exr_sequence(self) -> bool:
#         """pyseq를 이용해 EXR 시퀀스를 판별"""
#         seqs = pyseq.get_sequences(str(self.scan_path))
#         for seq in seqs:
#             if seq.extension.lower() == ".exr" and seq.length() >= 2:
#                 return True
#         return False

#     def is_mov_file(self) -> bool:
#         """MOV 파일이 하나만 존재하는지"""
#         mov_files = list(self.scan_path.glob("*.mov"))
#         return len(mov_files) == 1

#     def get_scan_type(self) -> str:
#         """
#         scan_path 내 데이터 타입 분석
#         Returns: "exr_sequence" | "mov" | "unknown"
#         """
#         if self.is_exr_sequence():
#             return "exr_sequence"
#         elif self.is_mov_file():
#             return "mov"
#         else:
#             return "unknown"

#     def get_exr_sequence_info(self):
#         """
#         EXR 시퀀스 정보 반환
#         Returns:
#             {
#                 "head": "plate.",
#                 "tail": ".exr",
#                 "start": 1001,
#                 "end": 1050,
#                 "pattern": "plate.%07d.exr",
#                 "length": 50
#             }
#         """
#         seqs = pyseq.get_sequences(str(self.scan_path))
#         for seq in seqs:
#             if seq.extension.lower() == ".exr":
#                 return {
#                     "head": seq.head(),
#                     "tail": seq.tail(),
#                     "start": seq.start(),
#                     "end": seq.end(),
#                     "pattern": f"{seq.head()}%0{seq.zfill()}d{seq.tail()}",
#                     "length": seq.length(),
#                 }
#         return None

from pathlib import Path
from collections import defaultdict


class FileManager:
    def __init__(self, scan_path: Path):
        self.scan_path = Path(scan_path)
        self.ext_map = {}  # 확장자별 파일 목록 캐시 (선택적)

    def collect_file_extensions(self) -> dict[str, list[Path]]:
        """
        폴더 내 파일들을 확장자별로 분류하여 딕셔너리로 반환
        예: {'.exr': [Path(...), ...], '.mov': [Path(...)]}
        """
        ext_dict = defaultdict(list)

        if not self.scan_path.exists() or not self.scan_path.is_dir():
            print(f"[WARN] 유효하지 않은 경로: {self.scan_path}")
            return {}

        for file in self.scan_path.iterdir():
            if file.is_file():
                ext = file.suffix.lower()
                ext_dict[ext].append(file)

        self.ext_map = dict(ext_dict)  # 내부 저장도 가능 (필요시)
        return self.ext_map


if __name__ == "__main__":
    from pprint import pprint

    scan_path = Path("/show/Constantine/product/scan/20241226/001_C014C018_230920_RO8N")
    file_mgr = FileManager(scan_path)
    ext_dict = file_mgr.collect_file_extensions()

    pprint(ext_dict)
    # 출력 예시:
    # {
    #   '.exr': [PosixPath(...), PosixPath(...)],
    #   '.mov': [PosixPath(...)]
    # }
