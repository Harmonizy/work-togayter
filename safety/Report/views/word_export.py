import os
from io import BytesIO
from datetime import date

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

from docx import Document
from docx.shared import Pt
from html2docx import html2docx

from ..models import BaseReport, AviationReport, GroundReport
from ..choices import ReportTypeChoices
from common.Services.thaidate import thai_date


def insert_html_at_paragraph(doc: Document, paragraph, html_content: str):
    """แทน ##content## ด้วย HTML ที่ render เป็น paragraph ลงไปแทน"""
    if not html_content:
        return

    # แปลง HTML → Document ชั่วคราว
    docx_stream = html2docx(html_content, title="My Document")
    temp_doc = Document(docx_stream)

    # index ของ paragraph ที่มี ##content##
    insert_index = doc.paragraphs.index(paragraph)

    # ลบข้อความเดิมออก
    paragraph.clear()

    # แทรก paragraph จาก HTML (เรียงจากล่างขึ้นบนเพื่อให้ตำแหน่งถูกต้อง)
    for para in reversed(temp_doc.paragraphs):
        new_para = doc.add_paragraph()
        for run in para.runs:
            r = new_para.add_run(run.text)
            r.bold = run.bold
            r.italic = run.italic
            r.underline = run.underline
            if run.font.color and run.font.color.rgb:
                r.font.color.rgb = run.font.color.rgb
            r.font.size = Pt(16)
            r.font.name = 'TH Sarabun New'

        # move new_para ไปที่ตำแหน่ง insert_index
        p = doc.paragraphs[-1]._element
        doc.paragraphs[insert_index]._element.addprevious(p)


def replace_placeholders_in_paragraphs(doc, context, base_report=None):
    # ใช้ copy list เพื่อไม่ให้กระทบตอน loop
    paragraphs = list(doc.paragraphs)

    for i, paragraph in enumerate(paragraphs):
        for key, value in context.items():
            if key in paragraph.text:
                if key == "##content##":
                    # ลบข้อความ placeholder
                    for run in paragraph.runs:
                        if key in run.text:
                            run.text = run.text.replace(key, "")

                    # แทรก HTML แทนที่
                    if base_report and base_report.content:
                        docx_stream = html2docx(base_report.content, title="Content")
                        temp_doc = Document(docx_stream)

                        insert_index = i + 1 

                        for para in reversed(temp_doc.paragraphs):
                            new_para = doc.add_paragraph()
                            for run in para.runs:
                                r = new_para.add_run(run.text)
                                r.bold = run.bold
                                r.italic = run.italic
                                r.underline = run.underline
                                if run.font.color and run.font.color.rgb:
                                    r.font.color.rgb = run.font.color.rgb
                                r.font.size = Pt(16)
                                r.font.name = 'TH Sarabun New'

                            # move paragraph มาที่ตำแหน่ง insert_index
                            p = doc.paragraphs[-1]._element
                            doc.paragraphs[insert_index-1]._element.addnext(p)

                else:
                    # placeholder ปกติ
                    for run in paragraph.runs:
                        if key in run.text:
                            run.text = run.text.replace(key, str(value))


def docx_to_response(doc, filename):
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@login_required
def safety_doc(request, pk):
    base_report = BaseReport.objects.get(id=pk)
    aviation_report = AviationReport.objects.filter(base_report=base_report).first()  # why why why why why
    ground_report = GroundReport.objects.filter(base_report=base_report).first()  # why why why why why

    BASE_TEMPLATE_DIR = os.path.join(settings.BASE_DIR, 'safety', 'Report', 'templates', 'Documents')

    report_type_to_template = {
        ReportTypeChoices.SIMPLE: 'hazard-report.docx',
        ReportTypeChoices.HAZARD_GROUND: 'ground-hazard-report.docx',
        ReportTypeChoices.HAZARD_AVIATION: 'aviation-hazard-report.docx',
        ReportTypeChoices.SAFETY_GROUND: 'ground-safety-report.docx',
        ReportTypeChoices.SAFETY_AVIATION: 'aviation-safety-report.docx',
        ReportTypeChoices.OBSERVATION: 'behavior-observation-report.docx',
    }

    template_filename = report_type_to_template.get(base_report.report_type, 'safety-report.docx')
    template_path = os.path.join(BASE_TEMPLATE_DIR, template_filename)

    doc = Document(template_path)

    base_context = {
        '##unit-short-name##': str(base_report.affiliation),
        '##title##': base_report.title or '',
        '##recorder##': str(base_report.recorder) if not base_report.anonymous else 'ไม่ระบุผู้ส่ง',
        '##position##': str(base_report.recorder.position) if not base_report.anonymous else '-',
        '##date##': thai_date(date.today()),
        '##report-type##': base_report.get_report_type_display() if base_report.report_type else '',
        'Rank': "พลอากาศตรี",
        'Name': "สุนทร สวัสดิ์",
        'Position': "ผู้อำนวยการกองบิน ๔",
        '##fiscal-year##': str(base_report.fiscal_year),
        '##affiliation##': str(base_report.affiliation),
        '##event-date##': thai_date(base_report.event_date),
        '##event-time##': base_report.event_time.strftime("%H:%M") if base_report.event_time else '',

        '##content##': '',  # จะถูกแทนด้วย HTML
        '##first_recommendation##': base_report.first_recommendation,
        '##initial_action_taken##': base_report.initial_action_taken,

        '##status##': base_report.get_status_display(),
        '##comment##': str(base_report.comment),
        '##created_at##': base_report.created_at,
        '##updated_at##': base_report.updated_at,

        '##example##': 'ตัวอย่าง ข้อความ',
    }

    ground_context = {}
    if hasattr(base_report, 'ground_report'):
        ground_report = base_report.ground_report
        ground_context = {
            '##location##': ground_report.location or '',
        }
        if ground_report and ground_report.category:
            ground_context['##category##'] = str(ground_report.category.name)

    air_context = {}
    if hasattr(base_report, 'aviation_report'):
        aviation_report = base_report.aviation_report
        air_context['##squadron##'] = str(aviation_report.squadron.name) if aviation_report.squadron else '-'
        air_context['##aircraft##'] = str(aviation_report.aircraft.name) if aviation_report.aircraft else '-'
        air_context['##flight_phase##'] = ', '.join(str(phase.name) for phase in aviation_report.flight_phase.all())

    context = {**base_context, **ground_context, **air_context}

    print("=== CONTEXT ===")
    for key, value in context.items():
        print(f"{key}: {value}")
    print("=== CONTEXT ===")

    # แทนค่าและจัดการ ##content##
    replace_placeholders_in_paragraphs(doc, context, base_report)

    return docx_to_response(doc, f"file-{template_filename}")
