from pathlib import Path
from typing import Optional


class PathManager:
    """Path와 관련된 이벤트 관리 경로지정 및 List 반환"""

    def __init__(self, show_root: str):
        self.show_root = Path(show_root)

        # Setting Path
        self.project_path: Optional[Path] = None
        self.scan_path: Optional[Path] = None
        self.selected_path: Optional[Path] = None
        # self.seq_path: Optional[Path] = None

    def get_project_list(self) -> list[str]:
        """show 경로의 폴더를 Project List로 반환"""

        project_list = sorted([p.name for p in self.show_root.iterdir() if p.is_dir()])
        # Path객체.iterdir(): 디렉토리 내의 항목들을 순회

        return project_list

    def project_to_path(self, project_name: str, arg):
        """Project와 인자를 받으면 path 지정"""

        self.project_path = self.show_root / project_name

        if arg == "scan":
            self.scan_path = self.project_path / "product" / "scan"
            return self.scan_path
        elif arg == "seq":
            self.seq_path = self.project_path / "seq"
        else:
            pass

    def get_scan_date_list(self) -> list[str]:
        """선택된 프로젝트의 scan 날짜 리스트 반환"""
        if not self.scan_path or not self.scan_path.exists():
            return []
        return sorted([p.name for p in self.scan_path.iterdir() if p.is_dir()])

    # def selected_to_path(self, selected_path: str, arg):
    #     """User가 선택한 원본 경로기반 경로지정"""

    #     if arg == "org":
    #         self.org_path = selected_path / "org"
    #     elif arg == "jpg":
    #         self.jpg_path = selected_path / "jpg"
    #     elif arg == "mov_to_exr":
    #         self.mov_to_exr_path = selected_path / "org" / "mov_to_exr"
    #     else:
    #         pass

    def seq_shot_to_path(self, seq_shot_path: str, arg):
        """User가 Seq / Shot Name 지정한뒤 경로지정"""

        if arg == "seq":
            self.seq_path = seq_shot_path
