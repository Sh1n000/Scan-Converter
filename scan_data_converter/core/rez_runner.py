# rez_runner.py
import subprocess
import shlex
from pathlib import Path
from typing import Sequence, Union


class RezRunner:
    """
    rez-env로 지정 패키지 환경을 활성화한 뒤, 명령을 실행
    """

    def __init__(self, packages: Sequence[str]):
        self.packages = list(packages)

    def run(
        self, cmd: Union[str, Sequence[str]], cwd: Union[str, Path] = None
    ) -> subprocess.CompletedProcess:
        # cmd가 문자열이면 shlex.split 으로 안전하게 토큰화
        parts = shlex.split(cmd) if isinstance(cmd, str) else list(cmd)
        rez_cmd = ["rez-env", *self.packages, "--", *parts]
        return subprocess.run(
            rez_cmd,
            cwd=str(cwd) if cwd is not None else None,
            capture_output=True,
            text=True,
            check=False,
        )
