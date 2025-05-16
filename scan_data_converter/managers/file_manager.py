from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Any
import pyseq
import json

from pyseq import Sequence


class FileManager:
    """
    1. User가 선택한 원본 Plate 경로 기반 Json 생성 [select_event.json]
       - exr seq / mov 판별
       - seq / shot name 정해지기전 상황
    2. Rename 기능
    3. Seq / Shot Name 정해진후 Json 재생성
    """

    def __init__(self, path: Path):
        if not path.exists() or not path.is_dir():
            raise ValueError(f"File Manager Path Error: {path}")
        self.path = path
        self.file_dict: Dict[str, List[Path]] = defaultdict(list)
        self.collect_by_extension()

    def collect_by_extension(self) -> Dict[str, List[Path]]:
        """확장자별로 파일을 수집"""
        self.file_dict.clear()
        for f in self.path.iterdir():
            if f.is_file():
                self.file_dict[f.suffix.lower()].append(f)
        return dict(self.file_dict)

    def is_exr_sequence(self) -> bool:
        """폴더 내 EXR 시퀀스 존재 여부 판별"""
        return len(self.get_exr_sequences()) > 0

    def is_mov(self) -> bool:
        """폴더 내 MOV 파일 존재 여부 판별"""
        return bool(self.file_dict.get(".mov"))

    def get_exr_sequences(self) -> List[Sequence]:
        """EXR 파일 중 Sequence 객체로 인식된 것만 필터링"""
        exr_files = self.file_dict.get(".exr", [])
        if not exr_files:
            return []

        raw = pyseq.get_sequences([str(f) for f in exr_files])
        # pyseq.get_sequences 결과에 문자열이 섞일 수 있음
        seqs: List[Sequence] = [s for s in raw if isinstance(s, Sequence)]
        return seqs

    def generate_select_event_json(self) -> Dict[str, Any]:
        """exr seq / mov 기반으로 초기 JSON 생성"""
        self.collect_by_extension()
        selected_dir = str(self.path)
        result: Dict[str, Any] = {"selected_dir": selected_dir}

        # EXR 시퀀스
        seqs = self.get_exr_sequences()
        if seqs:
            selected_data = [
                {
                    "pattern": seq.format(),
                    "start_frame": seq.start(),
                    "end_frame": seq.end(),
                    "frame_count": len(seq),
                }
                for seq in seqs
            ]
            event_info = [
                {
                    "org_path": str(
                        self.path / "org" / seq.format(),
                    ),
                    "jpg_path": str(self.path / "jpg" / "exr_to_jpg.%04d.jpg"),
                    "excel_path": str(self.path / "no_shot_name.xlsx"),
                }
                for seq in seqs[:1]
            ]
            result.update(
                {
                    "scan_type": "exr_seq",
                    "selected_data": selected_data,
                    "event_info": event_info,
                }
            )
            return result

        # MOV 처리
        mov_files = self.file_dict.get(".mov", [])
        if mov_files:
            selected_data = [{"file_name": f.name} for f in mov_files]
            event_info = [
                {
                    "org_path": str(self.path / "org" / mov_files[0].name),
                    "mov_to_exr_path": str(
                        self.path / "mov_to_exr" / f"{Path(mov_files[0]).stem}.%07d.exr"
                    ),
                    "jpg_path": str(self.path / "jpg" / "exr_to_jpg.%04d.jpg"),
                    "excel_path": str(self.path / "no_shot_name.xlsx"),
                }
            ]
            result.update(
                {
                    "scan_type": "mov",
                    "selected_data": selected_data,
                    "event_info": event_info,
                }
            )
            return result

        # 4) 기타
        result.update({"scan_type": "unknown", "selected_data": [], "event_info": []})
        return result

    def save_select_event_json(self, filename: str = "select_event.json") -> Path:
        """generate_select_event_json()를 파일로 저장하고 저장 경로 반환"""
        data = self.generate_select_event_json()
        out_path = self.path / filename
        out_path.write_text(self.to_json(data), encoding="utf-8")
        return out_path

    def save_initial_json(self, data: dict):
        json_dir = self.path
        # json_dir.mkdir(parents=True, exist_ok=True)
        out_file = json_dir / "initial_metadata.json"
        out_file.write_text(self.to_json(data), encoding="utf-8")

    def to_json(self, data: Any, **kwargs) -> str:
        """JSON 직렬화 헬퍼 메서드"""
        return json.dumps(data, ensure_ascii=False, indent=2, **kwargs)

    def generate_thumbnail(self):
        """jpg 시퀀스 Converting 후"""

        pass
