import subprocess
import json
from pathlib import Path
from typing import List, Dict, Union


class ExifManager:
    """
    exiftool을 사용해서 한 번에 여러 파일의 메타데이터를 JSON 형태로 추출합니다.
    """

    def __init__(self, exiftool_path: str = "exiftool"):
        self.exiftool_path = exiftool_path

    def extract_metadata(
        self, file_paths: List[Path]
    ) -> List[Dict[str, Union[str, int, float]]]:
        """
        file_paths: Path 또는 str 객체의 리스트
        반환값: 각 파일별 exiftool -j 출력(JSON) 파싱 결과 리스트
        -j : JSON형태로 출력

        """
        # 파일 경로를 문자열로 변환
        file_strs = [str(f) for f in file_paths]

        cmd = [self.exiftool_path, "-j", "-n", *file_strs]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise RuntimeError(f"Exiftool error:\n{result.stderr}")
        try:
            data = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 파싱 실패: {e}")
        return data
