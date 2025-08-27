import os
import pytest

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from ..models import BaseReport
from ..forms.reports import BaseReportForm


@pytest.mark.django_db
def test_requires_login(client):
    # ไม่ล็อกอิน → redirect ไป login
    url = reverse("report:safety-create.new_report")
    response = client.get(url)
    assert response.status_code == 302
    assert "/login" in response.url


@pytest.mark.django_db
def test_get_new_report(client, user):
    # GET → ต้อง render form และ formsets
    client.force_login(user)
    url = reverse("report:safety-create.new_report")
    response = client.get(url)
    
    assert response.status_code == 200
    assert "base_form" in response.context
    assert isinstance(response.context["base_form"], BaseReportForm)
    assert "image_formset" in response.context
    assert "recommendation_formset" in response.context
    assert "file_formset" in response.context


@pytest.mark.django_db
def test_post_report_success(client, user, mocker):
    # POST → สร้างสำเร็จ → redirect list
    client.force_login(user)
    url = reverse("report:safety-create.new_report")

    # Mock service ให้คืนค่า success
    mocker.patch(
        "safety.Report.views.safety_create.create_new_report",
        return_value=(True, (None, None, None, None), BaseReport())
    )

    response = client.post(url, {"priority": "LOW"})
    assert response.status_code == 302
    assert response.url == reverse("report:safety-report.list")


@pytest.mark.django_db
def test_post_report_fail(client, user, mocker):
    # POST → ไม่สำเร็จ → render form กลับ
    client.force_login(user)
    url = reverse("report:safety-create.new_report")

    base_form = BaseReportForm()
    forms = (base_form, base_form, base_form, base_form)
    response = client.post(url, {"priority": "INVALID"})
    assert response.status_code == 200
    assert "base_form" in response.context


@pytest.mark.django_db
def test_base_report_minimal_create(base_report):
    assert base_report.pk is not None
    assert base_report.title == "รายงานทดสอบ"
    # ตรวจ default
    assert base_report.report_type is not None
    assert base_report.event_date is not None
    assert base_report.event_time is not None


@pytest.mark.django_db
def test_image_upload_path(media_root, image_attachment, base_report):
    # ชื่อไฟล์ใน storage
    path = image_attachment.image.name
    assert "attachments" in path  # ตาม get_upload_to ของคุณ
    # ไฟล์ต้องถูกเซฟจริง ๆ
    abs_path = os.path.join(media_root, path)
    assert os.path.exists(abs_path)


@pytest.mark.django_db
def test_file_upload_path(media_root, file_attachment):
    path = file_attachment.file.name
    abs_path = os.path.join(media_root, path)
    assert os.path.exists(abs_path)


@pytest.mark.django_db
def test_recommendation_create(recommendation_attachment, base_report):
    assert recommendation_attachment.pk is not None
    assert recommendation_attachment.base_report_id == base_report.pk
    assert recommendation_attachment.note == "คำแนะนำเบื้องต้น"