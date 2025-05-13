# converters/base.py
from abc import ABC, abstractmethod
from pathlib import Path


class ConverterBackend(ABC):
    @abstractmethod
    def convert(self, input_path: Path, output_path: Path, **kwargs):
        """
        input_path 에 있는 파일을 output_path 형식으로 변환.
        """
        pass
