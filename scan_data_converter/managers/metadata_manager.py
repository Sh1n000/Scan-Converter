# managers/metadata_manager.py
import json
from pathlib import Path
from typing import List, Dict, Any


class MetadataManager:
    """
    추출된 메타데이터와 파일 정보를 모아 최종 JSON 테이블 구조로 관리합니다.
    records: List of dicts matching UI/Excel row 구조
    """

    def __init__(self):
        self.records: List[Dict[str, Any]] = []

    def add_record(
        self,
        seq_name: str,
        shot_name: str,
        version: str,
        org_type: str,
        scan_path: str,
        clip_name: str,
        metadata: Dict[str, Any],
        thumbnail: str = "",
        check: bool = False,
    ) -> None:
        record = {
            "check": check,
            "thumbnail": thumbnail,
            "seq_name": seq_name,
            "shot_name": shot_name,
            "version": version,
            "type": org_type,
            "scan_path": scan_path,
            "clip_name": clip_name,
            "metadata": metadata,
        }
        self.records.append(record)

    def to_json(self, indent: int = 2) -> str:
        """현재까지의 레코드를 JSON 문자열로 반환합니다."""
        return json.dumps(self.records, ensure_ascii=False, indent=indent)

    def save_json(self, out_path: Path, indent: int = 2) -> None:
        """파일로 저장합니다."""
        data = self.to_json(indent=indent)
        out_path.write_text(data, encoding="utf-8")
