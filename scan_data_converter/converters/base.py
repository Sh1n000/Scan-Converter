# converters/base.py
from pathlib import Path
from typing import Protocol, runtime_checkable


@runtime_checkable
class ConverterBackend(Protocol):
    """
    미디어 변환 백엔드 프로토콜
    convert(src, dst) → bool
    """

    def convert(self, src: Path, dst: Path) -> bool: ...
