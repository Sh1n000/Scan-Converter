import argparse
# from converters.exr_converter import ExrConverter # 미정 ffmpeg Converter / Nuke Converter로 변경될 수 있음

from managers.file_manager import FileManager


def main():
    parser = argparse.ArgumentParser(...)
    # --pattern, --input, --output 등 옵션 정의
    args = parser.parse_args()
    converter = ExrConverter(...)
    converter.run()


if __name__ == "__main__":
    main()

# 작업: 진입 스크립트를 작성하고 python scripts/convert_exr_to_jpg.py --help로 옵션이 잘 노출되는지 확인하세요.
