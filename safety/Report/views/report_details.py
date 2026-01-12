from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch, Count, Q
from django.contrib import messages
from django.http import HttpResponse

from ..models.reports import BaseReport, AviationReport, GroundReport, Participant, ReferenceReport
from ..models.attachments import Image, File, Recommendation
from ..choices import ReportTypeChoices
from safety.Report.models.sixA import SixA, Answer
from safety.Evaluate.models import BaseReportEvaluation, EvaluationAnswer


def is_type(report, type_choice):
    return report.report_type == type_choice

def is_type_in(report, choices):
    return report.report_type in choices


def has_report_permission_or_owner(view_func):
    def wrapper(request, pk):
        report = get_object_or_404(BaseReport, pk=pk)
        if request.user.has_perm("Report.view_all_report_detail") or report.recorder == request.user:
            return view_func(request, pk)

        if request.user.has_perm("Report.view_affiliation_report_detail"):
            if (report.affiliation == request.user.affiliation or report.location_affiliation == request.user.affiliation):
                return view_func(request, pk)
            else:
                raise PermissionDenied("คุณไม่มีสิทธิ์ดูรายงาน")
            
        raise PermissionDenied("คุณไม่มีสิทธิ์ดูรายงาน")
    return wrapper

# has_report_permission_or_owner(main_page)

@has_report_permission_or_owner
def main_page(request, pk):
    # report = get_object_or_404(BaseReport, pk=pk)

    # if request.user.has_perm("Report.view_all_report_detail"):
    #     pass
    # elif request.user.has_perm("Report.view_affiliation_report_detail"):
    #     if (
    #         report.affiliation != request.user.affiliation
    #         and report.location_affiliation != request.user.affiliation
    #     ):
    #         messages.error(request, "คุณไม่มีสิทธิ์ดูรายงานหน่วยอื่นได้")
    #         return redirect("report:safety-report.list")
    # elif report.recorder == request.user:
    #     pass
    # else:
    #     messages.error(request, "คุณไม่มีสิทธิ์ดูรายงานผู้อื่นได้")
    #     return HttpResponse(
    #         f"""
    #         ALL: {request.user.has_perm("Report.view_all_report_detail")}<br>
    #         AFF: {request.user.has_perm("Report.view_affiliation_report_detail")}<br>
    #         REC: {report.recorder == request.user}<br>
    #         APP: {report._meta.app_label}
    #         """
    #     )

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
        .select_related("base_report")
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

    sixA_all = SixA.objects.filter(report=report)

    sixA_answers = (
        Answer.objects
        .filter(sixA__in=sixA_all, answer=True)  # เฉพาะ True
        .select_related("question")
        .order_by("question__category", "question__code")
    )

    sixA_summary = (
        Answer.objects
        .filter(sixA__in=sixA_all)
        .values(
            "question__id",
            "question__code",
            "question__definition",
            "question__description",
            "question__category",
        )
        .annotate(
            true_count=Count("id", filter=Q(answer=True))
        )
        .filter(true_count__gt=0)   # เอาเฉพาะข้อที่มี True อย่างน้อย 1
        .order_by("question__category", "question__code")
    )

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

        "sixA_summary": sixA_summary,

        **flags,
        "is_missing_ground_report": flags["is_ground_report"] and not ground_report,
        "is_missing_aviation_report": flags["is_aviation_report"] and not aviation_report,
    }

    return render(request, "Report/safety-reports/detail/report-detail.html", context)
