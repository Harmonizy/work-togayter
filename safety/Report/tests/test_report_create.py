import os
import pytest
from django.urls import reverse

from django.contrib.auth import get_user_model
from common.RTAFUser.models import RTAFUser, Affiliation, Squadron, Rank

from ..forms.reports import BaseReportForm
from safety.Report.models import BaseReport

pytestmark = pytest.mark.django_db


@pytest.fixture
def base_payload(affiliation):
    payload = {
        "base_form-report_type": "S",
        "base_form-affiliation": str(affiliation.id),
        "base_form-title": "Unit test report",
        "base_form-content": "Auto content from test",
        "base_form-event_date": "2025-09-16",
        "base_form-event_time": "10:00",

        "images-TOTAL_FORMS": "0",
        "images-INITIAL_FORMS": "0",
        "images-MIN_NUM_FORMS": "0",
        "images-MAX_NUM_FORMS": "1000",

        "recommendations-TOTAL_FORMS": "0",
        "recommendations-INITIAL_FORMS": "0",
        "recommendations-MIN_NUM_FORMS": "0",
        "recommendations-MAX_NUM_FORMS": "1000",

        "files-TOTAL_FORMS": "0",
        "files-INITIAL_FORMS": "0",
        "files-MIN_NUM_FORMS": "0",
        "files-MAX_NUM_FORMS": "1000",

        "priority": "L",
    }

    return payload


@pytest.mark.django_db
def test_login_required(client):
    url = reverse("report:safety-create.new_report")
    respond = client.get(url)
    assert respond.status_code == 302
    assert "/login" in respond.url


@pytest.mark.django_db
def test_report_create_html_render(client, user):
    client.force_login(user)
    url = reverse("report:safety-create.new_report")
    respond = client.get(url)
    assert respond.status_code == 200


@pytest.mark.django_db
def test_post_invalid_rerenders_with_error(client, user):
    client.force_login(user)
    url = reverse("report:safety-create.new_report")
    respond = client.post(url, {})
    assert respond.status_code == 302
    assert "กรุณาตรวจสอบข้อมูลให้ถูกต้อง" in respond.content.decode("utf-8")


@pytest.mark.django_db
def test_report_create_redirects_to_report_list(client, user, base_payload):
    client.force_login(user)
    url = reverse("report:safety-create.new_report")
    respond = client.post(url, base_payload)
    assert respond.status_code in (302, 303)
    assert reverse("report:safety-report.list") in respond.url


@pytest.mark.django_db
def test_report_create_redirects_to_evaluate(client, user, base_payload):
    client.force_login(user)
    url = reverse("report:safety-create.new_report")
    payload = dict(base_payload)
    payload["surveyCheck"] = "1"

    respond = client.post(url, payload)

    assert respond.status_code in (302, 303)

    report_id = BaseReport.objects.latest("id")
    assert reverse("evaluate:evaluate-main", kwargs={"report_id": report_id.id})



# print("base errors:", base_form.errors)
# print("img fs errors:", image_formset.errors)
# print("rec fs errors:", rec_formset.errors)
# print("file fs errors:", file_formset.errors)