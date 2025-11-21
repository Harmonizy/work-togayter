import os
from io import BytesIO
from datetime import date
from bs4 import BeautifulSoup

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404
from docx.enum.text import WD_ALIGN_PARAGRAPH

from docx import Document
from docx.shared import Pt
from html2docx import html2docx

from ..models import BaseReport, AviationReport, GroundReport
from ..choices import ReportTypeChoices
from common.Services.thaidate import thai_date


# ---------------------------------------------------------
# 🔶 แปลงเลขอารบิก → ไทย
# ---------------------------------------------------------
def to_thai_digits(text: str) -> str:
    if not text:
        return text
    thai_map = str.maketrans("0123456789", "๐๑๒๓๔๕๖๗๘๙")
    return text.translate(thai_map)


# ---------------------------------------------------------
# 🔶 แปลงเลขไทยทั่วทั้งเอกสาร DOCX
# ---------------------------------------------------------
def convert_doc_numbers_to_thai(doc: Document):
    # paragraphs
    for p in doc.paragraphs:
        for run in p.runs:
            run.text = to_thai_digits(run.text)

    # tables
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    for run in p.runs:
                        run.text = to_thai_digits(run.text)


# ---------------------------------------------------------
# 🔶 ใส่ HTML ลง paragraph ใน docx
# ---------------------------------------------------------
def insert_html_at_paragraph(doc: Document, paragraph, html_content: str):
    if not html_content:
        return

    docx_stream = html2docx(html_content, title="My Document")
    temp_doc = Document(docx_stream)

    insert_index = doc.paragraphs.index(paragraph)

    paragraph.clear()

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

        p = doc.paragraphs[-1]._element
        doc.paragraphs[insert_index]._element.addprevious(p)


# ---------------------------------------------------------
# 🔶 แทนค่า placeholder + ใส่ HTML
# ---------------------------------------------------------
def replace_placeholders_in_paragraphs(doc, context, base_report=None):
    paragraphs = list(doc.paragraphs)

    for i, paragraph in enumerate(paragraphs):
        for key, value in context.items():
            if key in paragraph.text:
                if key == "##content##":
                    for run in paragraph.runs:
                        if key in run.text:
                            run.text = run.text.replace(key, "")

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

                            p = doc.paragraphs[-1]._element
                            doc.paragraphs[insert_index-1]._element.addnext(p)
                else:
                    for run in paragraph.runs:
                        if key in run.text:
                            run.text = run.text.replace(key, str(value))


# ---------------------------------------------------------
# 🔶 return file
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# 🔶 export safety report
# ---------------------------------------------------------
@login_required
def safety_doc(request, pk):
    base_report = BaseReport.objects.get(id=pk)

    aviation_report = AviationReport.objects.filter(base_report=base_report).first()
    ground_report = GroundReport.objects.filter(base_report=base_report).first()

    BASE_TEMPLATE_DIR = os.path.join(settings.BASE_DIR, 'safety', 'Report', 'templates', 'Documents')

    report_type_to_template = {
        ReportTypeChoices.SIMPLE: 'ground-safety-report.docx',
        ReportTypeChoices.HAZARD_GROUND: 'ground-incident-report.docx',
        ReportTypeChoices.HAZARD_AVIATION: 'aviation-hazard-report.docx',
        ReportTypeChoices.SAFETY_GROUND: 'ground-safety-report.docx',
        ReportTypeChoices.SAFETY_AVIATION: 'aviation-safety-report.docx',
        ReportTypeChoices.OBSERVATION: 'behavior-observation-report.docx',
    }

    template_filename = report_type_to_template.get(base_report.report_type, 'safety-report.docx')
    template_filename = 'ground-safety-report.docx'
    template_path = os.path.join(BASE_TEMPLATE_DIR, template_filename)

    doc = Document(template_path)

    base_context = {
        '##unit-short-name##': str(base_report.affiliation),
        '##title##': base_report.title or '',
        '##recorder##': str(base_report.recorder) if not base_report.anonymous else 'ไม่ระบุผู้ส่ง',
        '##position##': str(base_report.recorder.position) if not base_report.anonymous else '-',
        '##date##': thai_date(date.today()),
        '##report-type##': base_report.get_report_type_display() if base_report.report_type else '',
        'Rank': str(base_report.recorder.rank) if not base_report.anonymous else '-',
        'Name': str(base_report.recorder) if not base_report.anonymous else 'ไม่ระบุผู้ส่ง',
        'Position': str(base_report.recorder.position) if not base_report.anonymous else '-',
        '##fiscal-year##': str(base_report.fiscal_year),
        '##affiliation##': str(base_report.affiliation),
        '##event-date##': thai_date(base_report.event_date),
        '##event-time##': base_report.event_time.strftime("%H:%M") if base_report.event_time else '',
        '##content##': '',
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
        gr = base_report.ground_report
        ground_context = {
            '##location##': gr.location or '',
        }
        if gr and gr.category:
            ground_context['##category##'] = str(gr.category.name)

    air_context = {}
    if hasattr(base_report, 'aviation_report'):
        ar = base_report.aviation_report
        air_context['##squadron##'] = str(ar.squadron.name) if ar.squadron else '-'
        air_context['##aircraft##'] = str(ar.aircraft.name) if ar.aircraft else '-'
        air_context['##flight_phase##'] = ', '.join(str(phase.name) for phase in ar.flight_phase.all())

    context = {**base_context, **ground_context, **air_context}

    replace_placeholders_in_paragraphs(doc, context, base_report)

    # 🔶 แปลงเลขไทยทั่วเอกสารก่อนส่งออก
    convert_doc_numbers_to_thai(doc)

    return docx_to_response(doc, f"file-{template_filename}")


# ---------------------------------------------------------
# 🔶 insert HTML into message form
# ---------------------------------------------------------
def insert_html_to_docx(cell, html):
    soup = BeautifulSoup(html or "", "html.parser")

    for el in soup.children:
        if el.name in ["h1", "h2", "h3"]:
            p = cell.add_paragraph()
            run = p.add_run(el.get_text(strip=True))
            run.bold = True
            run.font.size = Pt(14)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT

        elif el.name == "p":
            p = cell.add_paragraph(el.get_text(strip=True))
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        elif el.name in ["ul", "ol"]:
            for li in el.find_all("li"):
                p = cell.add_paragraph(f"• {li.get_text(strip=True)}")
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        elif isinstance(el, str):
            if el.strip():
                p = cell.add_paragraph(el.strip())
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY


# ---------------------------------------------------------
# 🔶 export RTAF message form
# ---------------------------------------------------------
def rtaf_message_form(request, base_report_id):
    template_path = os.path.join(
        settings.BASE_DIR,
        'safety', 'Report', 'templates', 'Documents',
        'rtaf-message-form-template.docx'
    )
    doc = Document(template_path)

    base_report = get_object_or_404(BaseReport, id=base_report_id)

    ground = getattr(base_report, "groundreport", None)
    aviation = getattr(base_report, "aviationreport", None)
    participants = base_report.participants.all()

    commander_name = base_report.recorder.get_full_name() if base_report.recorder else "ไม่ระบุ"
    commander_rank = getattr(base_report.recorder.rank, "short_name", "") if hasattr(base_report.recorder, "rank") else ""
    commander_position = base_report.affiliation if base_report.affiliation else ""
    tel = base_report.affiliation.tel if hasattr(base_report.affiliation, "tel") else "ไม่ระบุ"

    report_body = ""
    if ground:
        report_body += f"สถานที่เกิดเหตุ: {ground.location or '-'}\n"
        report_body += f"ประเภทอุบัติเหตุ: {ground.get_accident_type_display() if ground.accident_type else '-'}\n"
    if aviation:
        report_body += f"หน่วยบิน: {aviation.squadron or '-'}\n"
        report_body += f"เครื่องบิน: {aviation.aircraft or '-'}\n"
    if participants.exists():
        report_body += "\nผู้เกี่ยวข้อง:\n"
        for p in participants:
            report_body += f"- {p.full_name or '-'} ({p.role or '-'}) [{p.get_injury_level_display() if p.injury_level else '-'}]\n"

    context = {
        '##report-title##': base_report.title,
        '##event-date-time##': f"{thai_date(base_report.event_date)} เวลา {base_report.event_time.strftime('%H:%M') if base_report.event_time else ''}",
        '##report-body##': report_body.strip() or base_report.content or "ไม่มีรายละเอียดเพิ่มเติม",
        '##sender-action##': "ด่วนที่สุด" if base_report.priority == "H" else "ด่วน",
        '##sender-info##': "ด่วนที่สุด" if base_report.priority == "H" else "ด่วน",
        '##secret-type##': "ลับมาก" if base_report.priority == "H" else "ลับ",
        '##action-list##': base_report.recorder.affiliation or "ไม่ระบุ",
        '##info-list##': "สนภ.ทอ., ศปก.ทอ.",
        '##name-drafter##': commander_name,
        '##office##': commander_position,
        '##tel##': tel,
        '##commander-rank##': commander_rank,
        '##commander-name##': commander_name,
        '##com-position##': commander_position,
        '##month-year##': thai_date(base_report.created_at.date()).split(" ")[-1],
        '##thai-pages##': '',
        '##eng-page##': '',
    }

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for run in paragraph.runs:
                        for key, value in context.items():
                            if key in run.text:
                                if key == '##report-body##':
                                    run.text = ""
                                    insert_html_to_docx(cell, value)
                                else:
                                    run.text = run.text.replace(key, str(value))

    # 🔶 แปลงเลขไทยทั้งไฟล์
    convert_doc_numbers_to_thai(doc)

    return docx_to_response(doc, f"rtaf-message-{base_report.id}.docx")
