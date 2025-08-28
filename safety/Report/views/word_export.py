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
        '##event-date##': thai_date(base_report.event_date) if base_report.event_date else '',
        '##event-time##': base_report.event_time.strftime("%H:%M") if base_report.event_time else '',
        '##squadron##': str(aviation_report.squadron) if getattr(aviation_report, 'squadron', None) else '',
        '##aircraft##': str(aviation_report.aircraft) if getattr(aviation_report, 'aircraft', None) else '',
        '##mission-type##': base_report.get_mission_type_display() if base_report.mission_type else '',
        '##report-type##': base_report.get_report_type_display() if base_report.report_type else '',
        '##location##': getattr(aviation_report, 'location', '') or '',
        '##injury-type##': getattr(aviation_report, 'injury_type', '') or '',
        '##damage-level##': getattr(aviation_report, 'damage_level', '') or '',
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
                    print(key, " xx ", f"'{run.text}'")
                    if key in run.text:
                        print("**match**")
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
    aviation_report = AviationReport.objects.filter(base_report=base_report).first()
    ground_report = GroundReport.objects.filter(base_report=base_report).first()

    BASE_TEMPLATE_DIR = os.path.join(settings.BASE_DIR, 'safety', 'Report', 'templates', 'Documents')

    report_type_to_template = {
        ReportTypeChoices.SIMPLE: 'safety-report.docx',
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
        '##date##': thai_date(date.today()),
        '##mission-type##': base_report.get_mission_type_display() if base_report.mission_type else '',
        '##report-type##': base_report.get_report_type_display() if base_report.report_type else '',
        
        '##fiscal-year##': str(base_report.fiscal_year),
        '##affiliation##': str(base_report.affiliation),
        '##event-date##': thai_date(base_report.event_date),
        '##event-time##': base_report.event_time.strftime("%H:%M") if base_report.event_time else '',
        
        '##content##': base_report.content,
        '##first_recommendation##': base_report.first_recommendation,
        '##initial_action_taken##': base_report.initial_action_taken,

        '##status##': base_report.get_status_display(),
        
        '##comment##': str(base_report.comment),
        '##created_at##': base_report.created_at,
        '##updated_at##': base_report.updated_at,
    }

    ground_context = {}

    if hasattr(base_report,'ground_report'):      
        ground_report = base_report.ground_report  
        ground_context = {
            '##location##': ground_report.location or  '',
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

    replace_placeholders_in_paragraphs(doc, context)

    if base_report.content:
        append_html_to_document(doc, base_report.content)

    return docx_to_response(doc, f"file-{template_filename}")
