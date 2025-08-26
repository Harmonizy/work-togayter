import os
import logging
from datetime import date

from django.conf import settings

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from openpyxl import load_workbook

from common.Services.docx_excel import find_replace, get_word_response, get_excel_response
from common.Services.thaidate import thai_date, thai_month_year

file_download_logger = logging.getLogger('mylogger.file_download')

def add_table_row(doc, grid_data):
    table = doc.tables[0]
    table.style = 'Table Grid'

    for i, row_data in enumerate(grid_data, 1):
        row = table.add_row()
        row.cells[0].text = f"{i}. {row_data['name']}"
        row.cells[1].text = row_data["status"]
        row.cells[2].text = f"{int(row_data['rate']):,}"
        
    for row in table.rows:
        for j, cell in enumerate(row.cells):
            paragraphs = cell.paragraphs
            for paragraph in paragraphs:
                for run in paragraph.runs:
                    font = run.font
                    font.size= Pt(16)
                    font.name = 'TH Sarabun New'
                if j > 0: paragraph.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER


def docx_example(request):
    docx_template = os.path.join(settings.BASE_DIR, "/app/common/RTAFUser/templates/RTAFUser/documents", "examples.docx")
    document = Document(docx_template)
    data_dict = {
        "keyword1": "value1",
        "keyword2": "value2",
        "keyword3": "value3",
        "date1": thai_date(date(2021, 1, 1)),
        "date2": thai_month_year(date(2024, 11, 12)),
        "month-year": thai_month_year(date.today()),
        "full_name": request.user.get_full_name() if request.user.is_authenticated else "John Doe",
        "mobile_phone": "08-1234-5678",
        "table_data": [
            {"name": "name1", "status": "status1", "rate": 1123},
            {"name": "name2", "status": "status2", "rate": 2234},
            {"name": "name3", "status": "status3", "rate": 3123},
        ]
    }

    find_replace(document, data_dict)
    add_table_row(document, data_dict["table_data"])
    file_download_logger.info(f"User {request.user} downloaded example.docx")
    return get_word_response(document, "example_report.docx")
    

def fill_excel_sheet(sheet, data, start_row=1):    
    for row_index, row_data in enumerate(data, start=start_row):
        for col_index, value in enumerate(row_data, start=1):
            cell = sheet.cell(row=row_index, column=col_index)
            cell.value = value


def excel_example(request):    
    template_path = os.path.join(settings.BASE_DIR, "/app/common/RTAFUser/templates/RTAFUser/documents", "examples.xlsx")    
    workbook = load_workbook(template_path)
    data_dict = {
        "unit_name": "หน่วย ศซว.ทอ.",
        "date": thai_date(date.today()),
        "table_data": [
                        ["1", "จอห์น โด", "อนุมัติ", "08-1234-5678"],
                        ["2", "เจน สมิธ", "รอดำเนินการ", "09-9876-5432"],
                        ["3", "อเล็กซ์ จอห์นสัน", "ถูกปฏิเสธ", "07-6543-3210"]
                    ]
    }

    sheet = workbook.active
    sheet["A1"] = data_dict["unit_name"]
    sheet["A2"] = data_dict["date"]
    
    fill_excel_sheet(sheet, data_dict["table_data"], start_row=4)
    file_download_logger.info(f"User {request.user} downloaded example.xlsx")
    return get_excel_response(workbook, "example_report.xlsx")