import os
from io import BytesIO
from datetime import date

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

from docx import Document
from docx.shared import Pt
from html2docx import html2docx

from ..models import BaseReport
from ..choices import ReportTypeChoices
from common.Services.thaidate import thai_date


def append_html_to_document(doc: Document, html_content: str) -> Document:
    docx_stream = html2docx(html_content, title="My Document")
    temp_doc = Document(docx_stream)
    
    for para in temp_doc.paragraphs:
        p = doc.add_paragraph()
        for run in para.runs:
            r = p.add_run(run.text)
            r.bold = run.bold
            r.italic = run.italic
            r.underline = run.underline
            if run.font.color and run.font.color.rgb:
                r.font.color.rgb = run.font.color.rgb
            r.font.size = Pt(16)
            r.font.name = 'TH Sarabun New'

    return temp_doc


def get_safety_report_context(base_report, safety_report):
    return {
        '##title##': base_report.title or '',
        '##fiscal-year##': str(base_report.fiscal_year),
        '##event-date##': thai_date(base_report.event_date),
        '##event-time##': base_report.event_time.strftime("%H:%M"),
        '##squadron##': str(safety_report.squadron) if safety_report.squadron else '',
        '##mission-type##': safety_report.get_mission_type_display() if safety_report.mission_type else '',
        '##report-type##': safety_report.get_report_type_display() if safety_report.report_type else '',
        '##aircraft##': str(safety_report.aircraft) if safety_report.aircraft else '',
        '##damage-level##': safety_report.get_damage_level_display() if safety_report.damage_level else '',
        '##injury-type##': safety_report.get_injury_type_display() if safety_report.injury_type else '',
        '##location##': str(safety_report.location) if safety_report.location else '',
        '##recorder##': base_report.recorder.get_full_name() if base_report.recorder else '',
        '##date##': thai_date(date.today()),
    }


def get_aviation_incident_report_context(base_report, aviation_report):
    return {
        '##title##': base_report.title or '',
        '##fiscal-year##': str(base_report.fiscal_year),
        '##event-date##': thai_date(base_report.event_date),
        '##event-time##': base_report.event_time.strftime("%H:%M"),
        '##squadron##': str(aviation_report.squadron) if aviation_report.squadron else '',
        '##aircraft##': str(aviation_report.aircraft) if aviation_report.aircraft else '',
        # Add other aviation-specific fields here
        '##recorder##': base_report.recorder.get_full_name() if base_report.recorder else '',
        '##date##': thai_date(date.today()),
    }


def get_ground_incident_report_context(base_report, ground_report):
    return {
        '##title##': base_report.title or '',
        '##fiscal-year##': str(base_report.fiscal_year),
        '##event-date##': thai_date(base_report.event_date),
        '##event-time##': base_report.event_time.strftime("%H:%M"),
        '##affiliation##': str(ground_report.affiliation) if ground_report.affiliation else '',
        '##location##': ground_report.location or '',
        '##category##': str(ground_report.category) if ground_report.category else '',
        '##anonymous##': "ใช่" if ground_report.anonymous else "ไม่ใช่",
        '##recorder##': base_report.recorder.get_full_name() if base_report.recorder else '',
        '##date##': thai_date(date.today()),
    }

def replace_placeholders_in_paragraphs(doc, context):
    for paragraph in doc.paragraphs:
        for key, value in context.items():
            if key in paragraph.text:
                for run in paragraph.runs:
                    if key in run.text:
                        run.text = run.text.replace(key, value)


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

    BASE_TEMPLATE_DIR = os.path.join(settings.BASE_DIR, 'safety', 'Report', 'templates','Documents')
    report_type_to_template = {
        ReportTypeChoices.SIMPLE: 'safety-report.docx',
        ReportTypeChoices.SAFETY_AVIATION: 'aviation-incident-report.docx',
        ReportTypeChoices.SAFETY_GROUND: 'ground-incident-report.docx',
    }

    template_path = os.path.join(BASE_TEMPLATE_DIR, report_type_to_template.get(base_report.report_type))

    doc = Document(template_path)

    if hasattr(base_report, 'safetyreport'):
        data_report = base_report.safetyreport
        context = get_safety_report_context(base_report, data_report)
        filename = f'safety-report-{pk}.docx'
    elif hasattr(base_report, 'AviationReport'):
        data_report = base_report.AviationReport
        context = get_aviation_incident_report_context(base_report, data_report)
        filename = f'aviation-incident-report-{pk}.docx'
    elif hasattr(base_report, 'GroundReport'):
        data_report = base_report.GroundReport
        context = get_ground_incident_report_context(base_report, data_report)
        filename = f'ground-incident-report-{pk}.docx'
    else:
        context = {
            '##title##': base_report.title or '',
            '##recorder##': base_report.recorder.get_full_name() if base_report.recorder else '',
            '##date##': thai_date(date.today()),
        }
        filename = f'report-{pk}.docx'

    replace_placeholders_in_paragraphs(doc, context)
    
    if base_report.content:
        append_html_to_document(doc, base_report.content)
        
    return docx_to_response(doc, filename)
