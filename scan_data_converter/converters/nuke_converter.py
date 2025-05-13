# converters/nuke_converter.py

from .base import ConverterBackend
from pathlib import Path
import subprocess


class NukeConverter(ConverterBackend):
    def convert(self, input_path: Path, output_path: Path, **kwargs):
        cmd = ["nuke", "-i", str(input_path), "-o", str(output_path)]
        subprocess.run(cmd, check=True)


# nuke_path = /opt/Nuke16.0v1/Nuke16.0
