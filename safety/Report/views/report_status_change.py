from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.contrib import messages

from .utils import card_data
from ..models import BaseReport
from ..choices import ReportStatusChoices, ReportTypeChoices
from ..rules import q_condition

from common.RTAFAuth.views import SuperAppLoginMixins
from common.RTAFUser.models import Affiliation

@login_required
@permission_required("Report.approve_report", raise_exception=True)
def approve_report(request, report_id):
    report = get_object_or_404(BaseReport, id=report_id)

    if report.status != ReportStatusChoices.APPROVE:
        report.status = ReportStatusChoices.APPROVE
        report.save()
        messages.success(request, f"อนุมัติรายงาน {report.title} เรียบร้อยแล้ว")
    else:
        messages.info(request, "รายงานนี้ได้รับการอนุมัติแล้ว")

    return redirect(reverse("report:safety-report.detail", kwargs={"pk": report.id}))


@login_required
@permission_required("Report.approve_report", raise_exception=True)
def reject_report(request, report_id):
    report = get_object_or_404(BaseReport, id=report_id)

    if report.status != ReportStatusChoices.REJECT:
        report.status = ReportStatusChoices.REJECT
        report.save()
        messages.warning(request, f"ไม่อนุมัติรายงาน {report.title}")
    else:
        messages.info(request, "รายงานนี้ถูกปฏิเสธแล้ว")

    return redirect(reverse("report:safety-report.detail", kwargs={"pk": report.id}))


@login_required
@permission_required("Report.approve_report", raise_exception=True)
def send_report(request, report_id):
    report = get_object_or_404(BaseReport, id=report_id)

    if report.status != ReportStatusChoices.SEND:
        report.status = ReportStatusChoices.SEND
        report.save()
        messages.warning(request, f"ส่งเรื่องสนภ.รายงาน {report.title}")
    else:
        messages.info(request, "รายงานนี้ถูกส่งเรื่องสนภ.แล้ว")

    return redirect(reverse("report:safety-report.detail", kwargs={"pk": report.id}))


@login_required
@permission_required("Report.approve_report", raise_exception=True)
def receive_report(request, report_id):
    report = get_object_or_404(BaseReport, id=report_id)

    if report.status != ReportStatusChoices.RECEIVE:
        report.status = ReportStatusChoices.RECEIVE
        report.save()
        messages.warning(request, f"สนภ.รับเรื่องรายงาน {report.title}")
    else:
        messages.info(request, "รายงานนี้ถูกสนภ.รับเรื่องแล้ว")

    return redirect(reverse("report:safety-report.detail", kwargs={"pk": report.id}))  


@login_required
@permission_required("Report.approve_report", raise_exception=True)
def complete_report(request, report_id):
    report = get_object_or_404(BaseReport, id=report_id)

    if report.status != ReportStatusChoices.COMPLETE:
        report.status = ReportStatusChoices.COMPLETE
        report.save()
        messages.warning(request, f"รายงาน {report.title} นี้เสร็จสิ้นแล้ว")
    else:
        messages.info(request, "รายงานนี้ถูกเสร็จสิ้นแล้ว")

    return redirect(reverse("report:safety-report.detail", kwargs={"pk": report.id}))


@login_required
@permission_required("Report.approve_report", raise_exception=True)
def archive_report(request, report_id):
    report = get_object_or_404(BaseReport, id=report_id)

    if report.status != ReportStatusChoices.ARCHIVE:
        report.status = ReportStatusChoices.ARCHIVE
        report.save()
        messages.warning(request, f"เก็บถาวรรายงาน {report.title}")
    else:
        messages.info(request, "รายงานนี้ถูกเก็บถาวรแล้ว")

    return redirect(reverse("report:safety-report.detail", kwargs={"pk": report.id}))


