# converters/media_converter.py
from pathlib import Path
from .base import ConverterBackend


class MediaConverter:
    """
    MediaConverter: ConverterBackend 를 주입받아
    src→dst 변환을 수행합니다.
    """

    def __init__(self, backend: ConverterBackend):
        self.backend = backend

    def convert(self, src: Path, dst: Path) -> bool:
        return self.backend.convert(src, dst)
