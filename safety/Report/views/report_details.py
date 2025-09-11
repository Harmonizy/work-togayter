from django.shortcuts import get_object_or_404, render
from django.db.models import Prefetch

from ..models.reports import BaseReport, AviationReport, GroundReport
from ..models.attachments import Image, File, Recommendation
from ..choices import ReportTypeChoices

from safety.Evaluate.models import BaseReportEvaluation, EvaluationAnswer

def _expect_flags(report_type: str):
    return {
        "is_ground": report_type in (ReportTypeChoices.SAFETY_GROUND, ReportTypeChoices.HAZARD_GROUND),
        "is_aviation": report_type in (ReportTypeChoices.SAFETY_AVIATION, ReportTypeChoices.HAZARD_AVIATION),
        "is_simple": report_type == ReportTypeChoices.SIMPLE,
        "is_observation": report_type == ReportTypeChoices.OBSERVATION,
    }

def main_page(request, pk: int):
    base_report = get_object_or_404(
        BaseReport.objects
        .prefetch_related(
            Prefetch('image_attachment', queryset=Image.objects.order_by('-created_at')),
            Prefetch('file_attachment', queryset=File.objects.order_by('-created_at')),
            Prefetch('recommendation_attachment', queryset=Recommendation.objects.order_by('-created_at')),
        )
        .select_related('affiliation', 'recorder'),
        pk=pk
    )

    aviation = (AviationReport.objects
                .select_related('base_report', 'squadron', 'aircraft')
                .prefetch_related('system', 'flight_phase')
                .filter(base_report=base_report)
                .first())

    ground = (GroundReport.objects
            .select_related('base_report', 'category')
            .filter(base_report=base_report)
            .first())

    evaluation = (BaseReportEvaluation.objects
                .select_related('final_result__type', 'question_set', 'evaluator', 'report')
                .prefetch_related(
                    Prefetch(
                        'answers',
                        queryset=EvaluationAnswer.objects
                                .select_related('question')
                                .order_by('order')
                    )
                )
                .filter(report=base_report)
                .first())

    flags = _expect_flags(base_report.report_type)

    context = {
        "base_report": base_report,
        "aviation": aviation,
        "ground": ground,
        "images": base_report.image_attachment.all(),
        "files": base_report.file_attachment.all(),
        "recommends": base_report.recommendation_attachment.all(),

        "evaluation": evaluation,
        "eval_answers": evaluation.answers.all() if evaluation else [],

        "report_type_label": base_report.get_report_type_display(),
        **flags,
        "missing_ground": flags["is_ground"] and not ground,
        "missing_aviation": flags["is_aviation"] and not aviation,
    }
    return render(request, "Report/safety-reports/report-detail.html", context)
