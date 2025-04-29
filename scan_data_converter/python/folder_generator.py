from pathlib import Path


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


# # 예시 실행
# if __name__ == "__main__":
#     project = ProjectStructureCreator("Constantine")
#     project.create_main_structure()
#     project.create_seq("s030")
#     project.create_seq("s040")
#     project.create_shot("s030", "0010")
#     project.print_structure_path()
