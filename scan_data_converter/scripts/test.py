import subprocess
import json
from pathlib import Path
from openpyxl import Workbook
from openpyxl.drawing.image import Image as XLImage
from PIL import Image
import tempfile


# 1. EXIFManager: EXR 시퀀스에서 메타데이터 추출
class ExifManager:
    def __init__(self, exiftool_path: str = "exiftool"):
        self.exiftool_path = exiftool_path

    def extract_json(self, file_paths):
        cmd = [self.exiftool_path, "-j", "-n"] + [str(p) for p in file_paths]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Exiftool error: {result.stderr}")
        return json.loads(result.stdout)


# 2. Thumbnail maker: 첫 프레임 JPG 생성
class ThumbnailMaker:
    def __init__(self, width=200, height=112):
        self.size = (width, height)

    def make_from_exr(self, exr_pattern, start_number=1001):
        # ffmpeg를 통해 첫 프레임만 JPG로 추출
        tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        cmd = [
            "ffmpeg",
            "-y",
            "-start_number",
            str(start_number),
            "-i",
            str(exr_pattern),
            "-frames:v",
            "1",
            tmp.name,
        ]
        subprocess.run(cmd, check=True)
        # PIL로 리사이즈
        with Image.open(tmp.name) as img:
            img.thumbnail(self.size)
            thumb_path = tmp.name.replace(".jpg", "_thumb.jpg")
            img.save(thumb_path)
        return thumb_path


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
    scan_dir = Path("/path/to/EXR_sequence")
    exr_files = sorted(scan_dir.glob("*.exr"))

    exif = ExifManager()
    metadata_list = exif.extract_json(exr_files)

    thumb_maker = ThumbnailMaker()
    excel = ExcelWriter(out_path="scan_metadata.xlsx")

    # 메타데이터 순회
    for md in metadata_list:
        thumb = thumb_maker.make_from_exr(
            exr_pattern=scan_dir / f"{md['FileName'].split('.')[0]}.%07d.exr"
        )
        excel.append_row(md, thumb)

    excel.save()
    print("Test complete: scan_metadata.xlsx generated with thumbnails.")
