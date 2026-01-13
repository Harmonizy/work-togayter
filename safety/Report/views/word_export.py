import os
import zipfile
import re

from io import BytesIO
from datetime import date
from bs4 import BeautifulSoup

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404

from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from html2docx import html2docx

from ..models import BaseReport, AviationReport, GroundReport
from ..choices import ReportTypeChoices
from common.Services.thaidate import thai_date


def convert_docx_numbers_everywhere(docx_bytes):
    thai_map = str.maketrans("0123456789", "๐๑๒๓๔๕๖๗๘๙")

    zin = zipfile.ZipFile(BytesIO(docx_bytes), 'r')
    zout_buffer = BytesIO()
    zout = zipfile.ZipFile(zout_buffer, 'w', zipfile.ZIP_DEFLATED)

    for item in zin.infolist():
        xml = zin.read(item.filename)

        if item.filename.endswith('.xml') or item.filename.endswith('.rels'):
            try:
                text = xml.decode('utf-8')
                text = re.sub(
                    r">([^<]+)<",
                    lambda m: ">" + m.group(1).translate(thai_map) + "<",
                    text
                )
                xml = text.encode('utf-8')
            except:
                pass

        zout.writestr(item, xml)

    zin.close()
    zout.close()
    return zout_buffer.getvalue()


def safe_insert_html(paragraph, html):
    if not html:
        return

    docx_stream = html2docx(html, title="HTMLContent")
    temp_doc = Document(docx_stream)

    runs_data = []
    for para in temp_doc.paragraphs:
        for run in para.runs:
            runs_data.append({
                "text": run.text,
                "bold": run.bold,
                "italic": run.italic,
                "underline": run.underline,
                "color": run.font.color.rgb if run.font.color else None
            })

    for r in paragraph.runs:
        r.text = ""

    for item in runs_data:
        r = paragraph.add_run(item["text"])
        r.bold = item["bold"]
        r.italic = item["italic"]
        r.underline = item["underline"]
        if item["color"]:
            r.font.color.rgb = item["color"]
        r.font.size = Pt(16)
        r.font.name = 'TH Sarabun New'


def replace_placeholders_in_paragraphs(doc, context, base_report=None):
    paragraphs = list(doc.paragraphs)

    for paragraph in paragraphs:
        for key, value in context.items():
            if key not in paragraph.text:
                continue

            if key == "##content##":
                for run in paragraph.runs:
                    run.text = run.text.replace(key, "")
                if base_report and base_report.content:
                    safe_insert_html(paragraph, base_report.content)
            else:
                for run in paragraph.runs:
                    if key in run.text:
                        run.text = run.text.replace(key, str(value))


def docx_to_response(doc, filename):
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    final_docx = convert_docx_numbers_everywhere(buffer.getvalue())

    response = HttpResponse(
        final_docx,
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
    response['Content-Disposition'] = f'attachment; filename="%s"' % filename
    return response


@login_required
def safety_doc(request, pk):
    base_report = BaseReport.objects.get(id=pk)
    aviation_report = AviationReport.objects.filter(base_report=base_report).first()
    ground_report = GroundReport.objects.filter(base_report=base_report).first()

    BASE_TEMPLATE_DIR = os.path.join(settings.BASE_DIR, 'safety', 'Report', 'templates', 'Documents')

    report_type_to_template = {
        ReportTypeChoices.SIMPLE: 'รายงานอันตราย.docx',

        ReportTypeChoices.HAZARD_GROUND: 'รายงานอันตรายภาคพื้น.docx',
        ReportTypeChoices.SAFETY_GROUND: 'รายงานอุบัติการณ์ภาคพื้น.docx',
        ReportTypeChoices.MINOR_ACCIDENT_GROUND: 'รายงานอันตราย.docx',
        ReportTypeChoices.MAJOR_ACCIDENT_GROUND: 'รายงานอันตราย.docx',

        ReportTypeChoices.HAZARD_AVIATION: 'รายงานอันตรายการบิน.docx',
        ReportTypeChoices.SAFETY_AVIATION: 'รายงานนิรภัยการบินขั้นต้น.docx',
        ReportTypeChoices.ANALYSIS_AVIATION: 'รายงานผลการวิเคราะห์อันตราย.docx',
        ReportTypeChoices.BIRD_AVIATION: 'รายงานอากาศยานชนนก.docx',
        ReportTypeChoices.FIX_ANALYSIS_AVIATION: 'รายงานข้อขัดข้องของการรายงานผลการวิเคราะห์อากาศยานอุบัติการณ์.docx',

        ReportTypeChoices.OBSERVATION: 'สังเกตการณ์พฤติกรรม.docx',
    }

    template_filename = report_type_to_template.get(base_report.report_type, 'รายงานอันตราย.docx')
    template_filename = 'รายงานอันตราย.docx'
    template_path = os.path.join(BASE_TEMPLATE_DIR, template_filename)

    doc = Document(template_path)

    base_context = {
        # '##unit-short-name##': str(base_report.affiliation),
        # '##title##': base_report.title or '',
        # '##recorder##': str(base_report.recorder) if not base_report.anonymous else 'ไม่ระบุผู้ส่ง',
        # '##position##': str(base_report.recorder.position) if not base_report.anonymous else '-',
        # '##date##': thai_date(date.today()),
        # '##report-type##': base_report.get_report_type_display() if base_report.report_type else '',
        # 'Rank': str(base_report.recorder.rank) if not base_report.anonymous else '-',
        # 'Name': str(base_report.recorder) if not base_report.anonymous else 'ไม่ระบุผู้ส่ง',
        # 'Position': str(base_report.recorder.position) if not base_report.anonymous else '-',
        '##fiscal-year##': str(base_report.fiscal_year),
        # '##affiliation##': str(base_report.affiliation),
        # '##event-date##': thai_date(base_report.event_date),
        # '##event-time##': base_report.event_time.strftime("%H:%M") if base_report.event_time else '',
        # '##content##': '',
        # '##first_recommendation##': base_report.first_recommendation,
        # '##initial_action_taken##': base_report.initial_action_taken,
        # '##status##': base_report.get_status_display(),
        # '##comment##': str(base_report.comment),
        # '##created_at##': base_report.created_at,
        # '##updated_at##': base_report.updated_at,
        '##fiscal_year##': str(base_report.fiscal_year),
        '##content##': '',
        '##recorder##': str(base_report.recorder) if not base_report.anonymous else 'ไม่ระบุผู้ส่ง',
        '##RTAFUser.position##': str(base_report.recorder.position) if not base_report.anonymous else '-',
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

    return docx_to_response(doc, f"file-{template_filename}")


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
                p = cell.add_paragraph("• " + li.get_text(strip=True))
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

        elif isinstance(el, str):
            if el.strip():
                p = cell.add_paragraph(el.strip())
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY


def rtaf_message_form(request, base_report_id):
    template_path = os.path.join(
        settings.BASE_DIR,
        'safety', 'Report', 'templates', 'Documents',
        'กระดานเขียนข่าว.docx'
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

    return docx_to_response(doc, f"rtaf-message-{base_report_id}.docx")
