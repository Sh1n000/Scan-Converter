from collections import defaultdict
from pathlib import Path
import pyseq
from pyseq import Sequence

# from pprint import pprint # 디버깅시 사용


class FileManager:
    """
    경로를 받아서 파일 Type 분석 후
    이동 및 파일명 변경
    """

    def __init__(self, scan_path: Path):
        self.scan_path = Path(scan_path)
        self.ext_map = {}  # 경로내 파일 확장자별로 분류된 딕셔너리

    def collect_file_extensions(self) -> dict[str, list[Path]]:
        """
        선택된 폴더 내 파일들을 확장자별로 분류하여 딕셔너리로 반환
        EX)  {'.exr': [Path(...), ...], '.mov': [Path(...)]}
        """
        ext_dict = defaultdict(list)

        if not self.scan_path.exists() or not self.scan_path.is_dir():
            print(
                f"[WARN] Scan Data Path Error (FM-collect_file_ext): {self.scan_path}"
            )
            return {}

        for file in self.scan_path.iterdir():
            if file.is_file():
                ext = file.suffix.lower()  # 확장자만 추출
                ext_dict[ext].append(file)

            print(file)

        self.ext_map = dict(ext_dict)  # defaultdict → dict 변환
        return self.ext_map

    def get_scan_type(self) -> str:
        """
        scan_path 내 데이터 타입 분석
        Returns: "exr_sequence" | "mov" | "unknown"
        """
        # 확장자 맵 먼저 수집
        if not self.ext_map:
            self.collect_file_extensions()

        # exr 확장자가 있을 때만 시퀀스 여부 판단
        if ".exr" in self.ext_map:
            if self.is_exr_sequence():
                return "exr_sequence"

        # mov 확장자가 있고, mov 파일이 1개만 있을 때
        if ".mov" in self.ext_map:
            if self.is_mov_file():
                return "mov"

        # 그 외는 unknown
        return "unknown"

    def is_mov_file(self) -> bool:
        """MOV 파일이 1개만 있는지 검사"""
        return len(self.ext_map.get(".mov", [])) == 1


if __name__ == "__main__":
    from pprint import pprint

    path = Path("/show/Constantine/product/scan/20241226/001_C014C018_230920_RO8N")
    fm = FileManager(path)

    print("[확장자 분석]")
    pprint(fm.collect_file_extensions())
