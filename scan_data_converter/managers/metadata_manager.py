from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Union
import json
import logging


@dataclass
class EXRMetadata:
    file_path: Path
    camera: str
    lens: str
    shutter: float
    iso: int
    # 필요에 따라 필드 추가


class MetadataManager:
    """
    EXR 또는 MOV 메타데이터 레코드를 관리하고 JSON / Excel로 저장하는 클래스
    """

    def __init__(self):
        self.records: List[EXRMetadata] = []

    def add_record(self, file_path: Path, data: Dict[str, Union[str, int, float]]):
        """
        데이터(dict)로부터 EXRMetadata 객체를 생성하여 records에 추가
        """
        record = EXRMetadata(
            file_path=file_path,
            camera=data.get("Camera", ""),
            lens=data.get("Lens", ""),
            shutter=data.get("ShutterSpeed", 0.0),
            iso=data.get("ISO", 0),
        )
        self.records.append(record)
        logging.debug(f"Added metadata record: {record}")

    def save_json(self, base_path: Path, filename: str = "metadata.json") -> Path:
        """
        records를 JSON 리스트로 직렬화하여 파일로 저장
        """
        json_dir = base_path / "metadata"
        json_dir.mkdir(parents=True, exist_ok=True)
        out_file = json_dir / filename
        # Path 객체를 문자열로 변환하여 JSON 직렬화 가능하게 만듭니다.
        data = [{**asdict(r), "file_path": str(r.file_path)} for r in self.records]
        out_file.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        logging.info(f"Saved metadata JSON at: {out_file}")
        return out_file

    def save_excel(self, base_path: Path, filename: str = "metadata.xlsx") -> Path:
        """
        pandas DataFrame으로 변환하여 Excel 파일로 저장
        pandas가 설치되어 있어야 합니다.
        """
        try:
            import pandas as pd
        except ImportError:
            raise RuntimeError(
                "pandas is required to save Excel files. `pip install pandas openpyxl` 설치하세요."
            )
        # DataFrame 변환 전 Path를 문자열로 변환
        records_dicts = [
            {**asdict(r), "file_path": str(r.file_path)} for r in self.records
        ]
        df = pd.DataFrame(records_dicts)
        excel_dir = base_path / "metadata"
        excel_dir.mkdir(parents=True, exist_ok=True)
        out_file = excel_dir / filename
        df.to_excel(out_file, index=False)
        logging.info(f"Saved metadata Excel at: {out_file}")
        return out_file
