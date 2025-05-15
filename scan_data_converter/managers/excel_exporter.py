# managers/excel_exporter.py
"""
최종 Excel(.xlsx) 파일 작성
1) pandas 또는 openpyxl 사용해 JSON 데이터를 DataFrame으로 변환
2) 썸네일 이미지 삽입한 Excel 파일(.xlsx) 작성
"""


class ExcelExporter:
    def export(self, records: list[EXRMetadata], out_path: Path):
        wb = Workbook()
        ws = wb.active
        # 헤더
        ws.append(["Thumbnail", "", "", "", "", ...])
        for r in records:
            ws.append([r.file_path.name, r.camera, r.lens, r.shutter, r.iso, ...])
        wb.save(out_path)
