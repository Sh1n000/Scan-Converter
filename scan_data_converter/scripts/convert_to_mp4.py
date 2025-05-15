import argparse
import subprocess
from pathlib import Path


def main():
    p = argparse.ArgumentParser("시퀀스를 MP4로 변환")
    p.add_argument(
        "--input",
        "-i",
        required=True,
        help="시퀀스 패턴 (예: '/…/%04d.jpg' or '/…/%07d.exr')",
    )
    p.add_argument(
        "--output", "-o", required=True, help="출력 비디오 경로 (예: '/…/out.mp4')"
    )
    p.add_argument("--start", "-s", type=int, default=1, help="시작 프레임 번호")
    p.add_argument("--framerate", "-r", type=int, default=24, help="프레임레이트")
    args = p.parse_args()

    cmd = [
        "ffmpeg",
        "-start_number",
        str(args.start),
        "-framerate",
        str(args.framerate),
        "-i",
        args.input,
        "-c:v",
        "libx264",
        "-pix_fmt",
        "yuv420p",
        str(args.output),
    ]
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
