# managers/metadata_manager.py

"""
EXR, MOV 메타데이터 추출 + 썸네일 생성
"""

@dataclass
class EXRMetadata:
    file_path: Path
    camera: str
    lens: str
    shutter: float
    iso: int
    # …필요한 필드 추가

class MetadataManager:
    def __init__(self):
        self.records: list[EXRMetadata] = []

    def add_record(self, file_path: Path, data: dict):
        # dict → EXRMetadata 변환 후 self.records.append(...)
