# managers/metadata_manager.py
import json
from pathlib import Path
from typing import List, Dict, Any

from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Union

# managers/metadata_manager.py
import json
import logging
import pandas as pd


class MetadataManager:
    """
    추출된 메타데이터와 파일 정보를 모아 최종 JSON 테이블 구조로 관리합니다.
    records: List of dicts matching UI/Excel row 구조
    """

    def __init__(self):
        self.records: List[Dict[str, Any]] = []

    def add_record(
        self,
        file_path: str,
        metadata: Dict[str, Any],
        thumbnail: str = "",
        check: bool = False,
    ) -> None:
        file_path = Path(file_path)
        seq_name = ""
        shot_name = ""
        version = str(metadata.get("version", ""))
        org_type = file_path.parent.name
        scan_path = str(file_path.parent)
        src_name = file_path.name

        width = metadata.get("ImageWidth")
        height = metadata.get("ImageHeight")

        resolution = f"{width}x{height}" if width and height else ""

        record = {
            "check": check,
            "thumbnail": thumbnail,
            "seq_name": seq_name,
            "shot_name": shot_name,
            "version": version,
            "type": org_type,
            "scan_path": scan_path,
            "src_name": src_name,
            "resolution": resolution,
        }
        self.records.append(record)

    def to_json(self, indent: int = 2) -> str:
        """현재까지의 레코드를 JSON 문자열로 반환합니다."""
        return json.dumps(self.records, ensure_ascii=False, indent=indent)

    def save_json(self, out_path: Path, indent: int = 2) -> None:
        """파일로 저장합니다."""
        data = self.to_json(indent=indent)
        out_path.write_text(data, encoding="utf-8")

    def save_excel(self, out_path: Path, filename: str) -> Path:
        """
        pandas DataFrame으로 변환하여 Excel 파일로 저장
        """

        # DataFrame 변환 전 Path를 문자열로 변환
        records_dicts = [
            {**asdict(r), "file_path": str(r.file_path)} for r in self.records
        ]
        df = pd.DataFrame(records_dicts)

        out_file = out_path / filename

        df.to_excel(out_file, index=False)
        logging.info(f"Saved metadata Excel at: {out_file}")
        return out_file
