# rez_runner.py
import subprocess

# import shlex
from pathlib import Path


class RezRunner:
    def __init__(self, packages: list[str]):
        self.packages = packages

    def run(self, cmd: list[str], cwd: Path = None):
        rez_cmd = ["rez-env", *self.packages, "--", *cmd]
        result = subprocess.run(
            rez_cmd,
            cwd=str(cwd) if cwd is not None else None,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(
                "RezRunner 실패:\n\n"
                f"--- STDOUT ---\n{result.stdout.strip()}\n\n"
                f"--- STDERR ---\n{result.stderr.strip()}"
            )
        return result.stdout
