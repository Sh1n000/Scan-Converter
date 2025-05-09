# /managers/exif_manager.py

"""
세부 구현:

subprocess + -json 옵션으로 한번에 여러 파일 처리

에러 핸들링(툴 미설치/권한 문제)

추출된 JSON → Python dict 으로 변환
"""


class ExifManager:
    def __init__(self, exiftool_path: str = "exiftool"):
        self.tool = exiftool_path

    def extract_metadata(self, file_paths: list[Path]) -> dict[Path, dict]:
        """
        각 파일별로 ExifTool 호출 후 JSON 파싱하여,
        {Path: {메타 필드: 값, ...}, ...} 반환
        """

        pass
