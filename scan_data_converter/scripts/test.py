import subprocess
import json
from pathlib import Path
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from PIL import Image
import tempfile
from managers.file_manager import FileManager

from typing import List, Dict, Any


# 1. EXIFManager: EXR 시퀀스에서 메타데이터 추출
class ExifManager:
    def __init__(self, exiftool_path: str = "exiftool"):
        self.exiftool_path = exiftool_path

    def extract_metadata(self, file_paths: List[Path]) -> Dict[str, Dict[str, Any]]:
        # 파일 경로를 문자열 리스트로 변환
        file_strs = [str(p) for p in file_paths]
        cmd = [self.exiftool_path, "-j", "-n", *file_strs]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Exiftool error: {result.stderr}")
        # JSON 문자열을 파이썬 객체(리스트 of dict)로 파싱해서 반환
        try:
            raw_list = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"JSON 파싱 오류: {e}\n출력:\n{result.stdout}")

        metadata: Dict[str, Dict[str, Any]] = {}

        for item in raw_list:
            source = item.pop("SourceFile", None)
            if source:
                metadata[source] = item

        return metadata


# 3. 엑셀 작성기: 메타+썸네일 삽입
class ExcelWriter:
    def __init__(self, out_path):
        self.wb = Workbook()
        self.ws = self.wb.active
        # 헤더
        self.ws.append(
            ["Seq", "Shot", "Version", "Type", "Scan Path", "Resolution", "Thumbnail"]
        )

    def append_row(self, data: dict, thumb_path: str):
        row_idx = self.ws.max_row + 1
        # 기본 텍스트 필드
        self.ws.append(
            [
                data.get("Seq Name", ""),
                data.get("Shot Name", ""),
                data.get("Version", ""),
                data.get("Type", ""),
                data.get("Scan Path", ""),
                f"{data.get('ImageWidth', '')}x{data.get('ImageHeight', '')}",
                "",
            ]
        )
        # 이미지 삽입
        img = XLImage(thumb_path)
        img.anchor = f"G{row_idx}"
        self.ws.add_image(img)

    def save(self):
        self.wb.save(
            filename=self.wb.filename if hasattr(self.wb, "filename") else out_path
        )


# 4. 테스트 실행: test.py
if __name__ == "__main__":
    # 테스트용 경로 설정
    p = "/show/Constantine/product/scan/20250515_1/097_A206C024_240315_R29Q"
    selected_fm = FileManager(Path(p))

    # 1) EXR 파일 리스트 수집
    exr_dict = selected_fm.collect_by_extension()
    exr_files = exr_dict[".exr"]  # 리스트

    try:
        exif_mgr = ExifManager()
        raw_meta_list = exif_mgr.extract_metadata(exr_files)
        # print(json.dumps(raw_meta_list, indent=2, ensure_ascii=False))
        # pprint.pprint(raw_meta_list)

    except RuntimeError as e:
        print(f"오류 발생: {e}")

    # 썸네일 경로지정

    excel = ExcelWriter(out_path="scan_metadata.xlsx")

    # # 메타데이터 순회
    # for md in metadata_list:
    #     thumb = thumb_maker.make_from_exr(
    #         exr_pattern=scan_dir / f"{md['FileName'].split('.')[0]}.%07d.exr"
    #     )
    #     excel.append_row(md, thumb)

    # excel.save()
    # print("Test complete: scan_metadata.xlsx generated with thumbnails.")
