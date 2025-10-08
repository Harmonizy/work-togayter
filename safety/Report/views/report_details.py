from django.shortcuts import get_object_or_404, render
from django.db.models import Prefetch

from ..models.reports import BaseReport, AviationReport, GroundReport, Participant, ReferenceReport
from ..models.attachments import Image, File, Recommendation
from ..choices import ReportTypeChoices

from safety.Evaluate.models import BaseReportEvaluation, EvaluationAnswer


def is_type(report, type_choice):
    return report.report_type == type_choice

def is_type_in(report, choices):
    return report.report_type in choices


def main_page(request, pk):
    report = get_object_or_404(
        BaseReport.objects
            .select_related("affiliation", "recorder")
            .prefetch_related(
                Prefetch("image_attachment", queryset=Image.objects.order_by("-created_at")),
                Prefetch("file_attachment", queryset=File.objects.order_by("-created_at")),
                Prefetch("recommendation_attachment", queryset=Recommendation.objects.order_by("-created_at")),
                Prefetch("participants", queryset=Participant.objects.select_related("role").order_by("id")),
                Prefetch("references", queryset=ReferenceReport.objects.select_related("report").order_by("id")),
            ),
        pk=pk
    )

    aviation_report = (
        AviationReport.objects
        .filter(base_report=report)
        .select_related("base_report", "squadron", "aircraft")
        .prefetch_related("system", "flight_phase")
        .first()
    )

    ground_report = (
        GroundReport.objects
        .filter(base_report=report)
        .select_related("base_report", "category")
        .first()
    )

    evaluation = (
        BaseReportEvaluation.objects
        .filter(report=report)
        .select_related("final_result__type", "question_set", "evaluator", "report")
        .prefetch_related(
            Prefetch(
                "answers",
                queryset=EvaluationAnswer.objects.select_related("question").order_by("order")
            )
        )
        .first()
    )

    flags = {
        "is_ground_report": is_type_in(report, [ReportTypeChoices.SAFETY_GROUND, ReportTypeChoices.HAZARD_GROUND]),
        "is_aviation_report": is_type_in(report, [ReportTypeChoices.SAFETY_AVIATION, ReportTypeChoices.HAZARD_AVIATION]),
        "is_simple_report": is_type(report, ReportTypeChoices.SIMPLE),
        "is_observation_report": is_type(report, ReportTypeChoices.OBSERVATION),
    }

    context = {
        "base_report": report,
        "aviation_report": aviation_report,
        "ground_report": ground_report,

        "images": report.image_attachment.all(),
        "files": report.file_attachment.all(),
        "recommendations": report.recommendation_attachment.all(),

        "participants": report.participants.all(),
        "reference_reports": report.references.all(),

        "evaluation": evaluation,
        "evaluation_answers": evaluation.answers.all() if evaluation else [],
        "report_type_label": report.get_report_type_display(),

        **flags,
        "is_missing_ground_report": flags["is_ground_report"] and not ground_report,
        "is_missing_aviation_report": flags["is_aviation_report"] and not aviation_report,
    }

    return render(request, "Report/safety-reports/detail/report-detail.html", context)
