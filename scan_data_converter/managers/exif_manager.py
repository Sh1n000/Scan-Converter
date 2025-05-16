# managers/exif_manager.py
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Any


class ExifManager:
    """
    exiftool을 사용해서 여러 파일의 메타데이터를 JSON 형태로 추출합니다.
    반환값: 파일 경로 문자열을 키로, 해당 파일의 메타데이터 딕셔너리를 값으로 갖는 dict
    """

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
