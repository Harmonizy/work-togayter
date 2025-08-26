from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages

from ..models import BaseReport

def delete_report(request, pk):
    report = get_object_or_404(BaseReport, pk=pk)
    title = report.title
    if request.method == "POST":
        report.delete()
        messages.success(request, f"ลบรายงาน{title} เรียบร้อยแล้ว")
        
    return redirect(reverse("report:safety-report.list"))
