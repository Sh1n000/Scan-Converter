# converters/nuke_converter.py
from pathlib import Path
from core.rez_runner import RezRunner
from .base import ConverterBackend


class NukeConverter(ConverterBackend):
    """Nuke 기반 미디어 변환 백엔드"""

    def __init__(self, rez_pkgs: list[str] = ["nuke", "python-3.9"]):
        self.rez = RezRunner(rez_pkgs)

    def convert(self, src: Path, dst: Path) -> bool:
        cmd = [
            "nuke",
            "-ix",
            "/path/to/your_nuke_script.py",
            "--read",
            str(src),
            "--write",
            str(dst),
        ]
        result = self.rez.run(cmd)
        if result.returncode != 0:
            print(f"[NukeConverter] Error:\n{result.stderr}")
            return False
        return True
