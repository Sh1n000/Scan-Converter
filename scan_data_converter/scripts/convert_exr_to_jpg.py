# #!/usr/bin/env python3
# # scripts/convert_exr_to_jpg.py

# import argparse
# import sys
# from pathlib import Path

# from pyseq import Sequence

# from managers.file_manager import FileManager
# from converters.media_converter import MediaConverter


# def parse_args():
#     parser = argparse.ArgumentParser(description="EXR 시퀀스를 JPG로 변환하는 유틸리티")
#     parser.add_argument(
#         "-p",
#         "--pattern",
#         required=True,
#         help="시퀀스 패턴 (예: 'C014C018_230920_RO8N.%07d.exr')",
#     )
#     parser.add_argument("-i", "--input", required=True, help="입력 디렉토리 경로")
#     parser.add_argument("-o", "--output", required=True, help="출력 디렉토리 경로")
#     parser.add_argument(
#         "-s", "--start", type=int, help="변환 시작 프레임 (기본: 시퀀스 전체)"
#     )
#     parser.add_argument(
#         "-e", "--end", type=int, help="변환 종료 프레임 (기본: 시퀀스 전체)"
#     )
#     return parser.parse_args()


# def main():
#     args = parse_args()

#     input_dir = Path(args.input)
#     output_dir = Path(args.output)

#     # 1) FileManager 로 폴더 준비
#     fm = FileManager(input_dir)
#     fm.ensure_dir(output_dir)

#     # 2) pyseq 로 패턴 인식
#     try:
#         seq = Sequence(args.pattern, dir=input_dir)
#     except Exception as e:
#         print(f"패턴 인식 오류: {e}", file=sys.stderr)
#         sys.exit(1)

#     # 3) 프레임 범위 결정
#     start = args.start or seq.start
#     end = args.end or seq.end

#     # 4) ffmpeg Converter 래핑된 MediaConverter 준비
#     converter = MediaConverter(rez_pkgs=["ffmpeg"])

#     # 5) 시퀀스 전체 변환
#     converter.convert_sequence(
#         sequence=seq,
#         output_dir=output_dir,
#         start_frame=start,
#         end_frame=end,
#     )

#     print(f"변환 완료: {input_dir}/{args.pattern} → {output_dir} ({start}-{end})")


# if __name__ == "__main__":
#     main()
