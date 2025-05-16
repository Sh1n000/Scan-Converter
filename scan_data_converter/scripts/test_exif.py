# test_run_exif.py
import subprocess
import json
from pathlib import Path
from managers.exif_manager import ExifManager
from managers.metadata_manager import MetadataManager
from managers.file_manager import FileManager
from pathlib import Path

# import pprint
import pandas as pd

from IPython.display import display


if __name__ == "__main__":
    """
    Meta Data 생성 (JSON & 엑셀)
    """
    p = "/show/Constantine/product/scan/20250509/001_C014C018_230920_RO8N/org"
    selected_path = Path(p)
    selected_fm = FileManager(selected_path)

    # 1) EXR 파일 리스트 수집
    exr_dict = selected_fm.collect_by_extension()
    exr_files = exr_dict[".exr"]  # 리스트

    # 2) ExifManager로 메타데이터 추출

    try:
        exif_mgr = ExifManager()
        raw_meta_list = exif_mgr.extract_metadata(exr_files)
        # print(json.dumps(raw_meta_list, indent=2, ensure_ascii=False))
        # pprint.pprint(raw_meta_list)

    except RuntimeError as e:
        print(f"오류 발생: {e}")

    df = pd.DataFrame(raw_meta_list)
    display(df)

    # 빈 컬럼 추가
    # df["seq_name"] = ""
    # df["shot_name"] = ""
    # df["type"] = "org"
    # df["version"] = ""
    # df["scan_path"] = ""
    # df.to_excel("scan_list.xlsx", index=False)

    # # 3) MetadataManager에 맵핑 & 저장
    # meta_mgr = MetadataManager()
    # for src_path, meta in raw_meta_list.items():
    #     meta_mgr.add_record(src_path, meta)  # src_path -> str

    # # JSON 출력
    # print(meta_mgr.to_json())

    # # pprint.pprint(meta_mgr.records)

    # # # 4) JSON 또는 Excel로 출력
    # # meta_mgr.save_json(selected_path)

    # # meta_mgr.save_excel(selected_path)

    # # 메타데이터 추출
