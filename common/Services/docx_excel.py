import os
from io import BytesIO

from django.http import HttpResponse

from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH


def find_replace(document, data_dict):        
    for paragraph in document.paragraphs:
        for key, value in data_dict.items():
            if key in paragraph.text:
                inline_shapes = paragraph.runs  
                for run in inline_shapes:
                    try:
                        if key in run.text:
                            run.text = run.text.replace(key, value)
                    except:
                        pass


def set_table_style(table):    
    for row in table.rows:
        for cell in row.cells:            
            for paragraph in cell.paragraphs:
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in paragraph.runs:
                    font = run.font
                    font.size = Pt(16)  
                    font.name = 'TH Sarabun New'  


def get_file_response(file_content, content_type, filename):
    response = HttpResponse(content_type=content_type)
    file_content.save(response)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'    
    return response


def get_word_response(document, filename="document.docx"):
    return get_file_response(document, "application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename)


def get_excel_response(workbook, filename="spreadsheet.xlsx"):
    return get_file_response(workbook, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename)
