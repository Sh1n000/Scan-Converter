from pathlib import Path
import logging  # Dir Mgr
import shutil  # Dir Mgr
from typing import Union


class ProjectStructureCreator:
    def __init__(self, project_name: str, base_path: str = ""):
        if not project_name:
            raise ValueError("Project 이름을 지정해주세요.")

        self.project_name = project_name
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.root = self.base_path / self.project_name

        self.structure = {
            "_3d": [],
            "assets": [],
            "config": [],
            "preproduction": [
                "assets",
                "concept",
                "previz",
                "ref",
                "seq",
                "shot_test",
                "techviz",
            ],
            "product": ["daily", "doc", "edit", "in", "out", "ref", "scan", "tmp"],
            "seq": [],
            "shotgun_toolkit": [],
            "tmp": [],
        }

    def create_main_structure(self):
        print(f"[+] Creating project at: {self.root}")
        for folder, subfolders in self.structure.items():
            current_path = self.root / folder
            current_path.mkdir(parents=True, exist_ok=True)
            for sub in subfolders:
                (current_path / sub).mkdir(parents=True, exist_ok=True)

    def create_seq_dir(self, seq_name: str):
        if not seq_name:
            raise ValueError("Sequence name 이 없습니다.")
        seq_path = self.root / "seq" / seq_name
        seq_path.mkdir(parents=True, exist_ok=True)
        print(f"[+] Created sequence folder: {seq_path}")

    def create_shot_dir(self, seq_name: str, shot_number: str):
        """
        seq_name 과 shot_number가 정해지면 Shot folder 생성
        EX) seq_name : s030 / shot_number : 0010
        """
        if not seq_name or not shot_number:
            raise ValueError("Sequence name 과 Shot number 가 모두 필요합니다.")

        shot_name = f"{seq_name}_{shot_number}"
        shot_path = self.root / "seq" / seq_name / shot_name
        shot_path.mkdir(parents=True, exist_ok=True)
        print(f"[+] Created shot folder: {shot_path}")

    def print_structure_path(self):
        print(f"[+] Root: {self.root}")
        self._print_tree(self.root)

    def _print_tree(self, path: Path, prefix: str = ""):
        print(prefix + path.name + "/")
        for p in sorted(path.iterdir()):
            if p.is_dir():
                self._print_tree(p, prefix + "    ")


# # Project Structure 예시 실행
# if __name__ == "__main__":
#     project = ProjectStructureCreator("RND")
#     project.create_main_structure()
#     # project.create_seq("s030")
#     # project.create_seq("s040")
#     # project.create_shot("s030", "0010")
#     project.print_structure_path()


class DirectoryManager:
    """
    주어진 경로의 부모 디렉토리가 실존할 때에만,
    자신(또는 파일의 부모)을 생성해 주는 클래스.
    """

    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            fmt = "%(asctime)s %(levelname)s %(message)s"
            handler.setFormatter(logging.Formatter(fmt))
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def ensure_directory(
        self, path: Union[str, Path], exist_ok: bool = True, parents: bool = True
    ) -> Path:
        """
        path가 가리키는 디렉토리가 없으면 생성하고, Path 객체를 반환.
        부모 디렉토리가 없으면 ValueError 발생.
        """
        p = Path(path)
        # p가 파일 경로(확장자 포함)라면 부모 폴더를, 아니면 자기 자신을 디렉토리 경로로 본다
        dir_path = p.parent if p.suffix else p

        parent = dir_path.parent
        if not parent.exists():
            raise ValueError(f"유효하지 않은 부모 경로입니다: {parent!r}")

        dir_path.mkdir(parents=parents, exist_ok=exist_ok)
        self.logger.info(f"Directory ready: {dir_path}")
        return dir_path

    def move_file(
        self, src: Union[str, Path], dst: Union[str, Path], overwrite: bool = False
    ) -> Path:
        """
        src 파일을 dst 위치로 이동(mv)합니다.
        - dst의 부모 디렉토리가 없으면 생성.
        - overwrite=False 이고 dst가 존재하면 FileExistsError 발생.
        - overwrite=True 이면 기존 파일을 덮어쓰고 이동.

        Returns:
            Path: 이동된 파일의 최종 경로
        """
        src_path = Path(src)
        dst_path = Path(dst)
        if not src_path.exists() or not src_path.is_file():
            raise FileNotFoundError(f"이동할 파일이 없습니다: {src_path!r}")

        # dst의 부모 폴더가 있어야 하므로, ensure_directory 호출
        self.ensure_directory(dst_path.parent, exist_ok=True, parents=True)

        # 덮어쓰기 처리
        if dst_path.exists():
            if overwrite:
                dst_path.unlink()  # 기존 파일 삭제
            else:
                raise FileExistsError(f"목적지에 이미 파일이 존재합니다: {dst_path!r}")

        # 실제 이동
        shutil.move(str(src_path), str(dst_path))
        # self.logger.info(f"Moved file: {src_path} → {dst_path}")
        print("이동완료")
        return dst_path
