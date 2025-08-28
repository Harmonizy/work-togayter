import os
import pytest
from django.urls import reverse

from ..forms.reports import BaseReportForm

@pytest.mark.django_db
def test_requires_login(client):
    url = reverse("report:safety-create.new_report")
    resp = client.get(url)
    assert resp.status_code == 302
    assert "/login" in resp.url

@pytest.mark.django_db
def test_get_new_report(client, user):
    client.force_login(user)
    url = reverse("report:safety-create.new_report")
    resp = client.get(url)
    assert resp.status_code == 200
    assert "base_form" in resp.context
    assert isinstance(resp.context["base_form"], BaseReportForm)
    assert "image_formset" in resp.context
    assert "recommendation_formset" in resp.context
    assert "file_formset" in resp.context

# --------------------------
# 🔧 Fixtures (ปรับ prefix ให้ตรง view)
# --------------------------
@pytest.fixture
def base_form_minimal_fields(affiliation):
    return {
        "base_form-title": "รายงานใหม่",
        "base_form-priority": "LOW",
        "base_form-event_date": "2025-08-01",
        "base_form-event_time": "10:00:00",
        "base_form-affiliation": affiliation.pk if affiliation else "",
        "base_form-report_type": "S",
        "base_form-content": "สำหรับทดสอบ",
    }

@pytest.fixture
def empty_formsets_payload():
    return {
        # images
        "images-TOTAL_FORMS": "0",
        "images-INITIAL_FORMS": "0",
        "images-MIN_NUM_FORMS": "0",
        "images-MAX_NUM_FORMS": "1000",

        # recommendations
        "recommendations-TOTAL_FORMS": "0",
        "recommendations-INITIAL_FORMS": "0",
        "recommendations-MIN_NUM_FORMS": "0",
        "recommendations-MAX_NUM_FORMS": "1000",

        # files
        "files-TOTAL_FORMS": "0",
        "files-INITIAL_FORMS": "0",
        "files-MIN_NUM_FORMS": "0",
        "files-MAX_NUM_FORMS": "1000",
    }

@pytest.fixture
def payload_new_report_success(base_form_minimal_fields, empty_formsets_payload):
    data = {}
    data.update(base_form_minimal_fields)
    data.update(empty_formsets_payload)
    return data

@pytest.fixture
def payload_new_report_fail(empty_formsets_payload):
    data = {
        "base_form-title": "รายงานไม่ครบ",
        "base_form-priority": "INVALID",  # ทำให้ invalid
        "base_form-event_date": "2025-08-01",
        "base_form-event_time": "10:00:00",
    }
    data.update(empty_formsets_payload)
    return data

# --------------------------
# ✅ Tests
# --------------------------
@pytest.mark.django_db
def test_post_report_success(client, user, payload_new_report_success):
    client.force_login(user)
    url = reverse("report:safety-create.new_report")
    resp = client.post(url, payload_new_report_success)

    # Debug ช่วยไล่ error เวลาแดง (ลบออกได้)
    if resp.status_code != 302 and hasattr(resp, "context") and resp.context:
        bf = resp.context.get("base_form")
        img = resp.context.get("image_formset")
        rec = resp.context.get("recommendation_formset")
        fil = resp.context.get("file_formset")
        print("BASE ERRORS:", getattr(bf, "errors", None))
        print("IMG ERRORS:", getattr(img, "errors", None), getattr(img, "non_form_errors", lambda: None)())
        print("REC ERRORS:", getattr(rec, "errors", None), getattr(rec, "non_form_errors", lambda: None)())
        print("FILE ERRORS:", getattr(fil, "errors", None), getattr(fil, "non_form_errors", lambda: None)())

    assert resp.status_code == 302
    assert resp.url == reverse("report:safety-report.list")

@pytest.mark.django_db
def test_post_report_fail(client, user, payload_new_report_fail):
    client.force_login(user)
    url = reverse("report:safety-create.new_report")
    resp = client.post(url, payload_new_report_fail)
    assert resp.status_code == 200
    assert "base_form" in resp.context

# -------- พวก test อื่น ๆ ของคุณคงเดิม --------

@pytest.mark.django_db
def test_base_report_minimal_create(base_report):
    assert base_report.pk is not None
    assert base_report.title == "รายงานทดสอบ"
    assert base_report.report_type is not None
    assert base_report.event_date is not None
    assert base_report.event_time is not None

@pytest.mark.django_db
def test_image_upload_path(media_root, image_attachment, base_report):
    path = image_attachment.image.name
    assert "attachments" in path
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
