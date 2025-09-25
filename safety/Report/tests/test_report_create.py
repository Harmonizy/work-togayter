import os
import pytest
from django.urls import reverse

from django.contrib.auth import get_user_model
from common.RTAFUser.models import RTAFUser, Affiliation, Squadron, Rank

from ..forms.reports import BaseReportForm
from safety.Report.models import BaseReport

pytestmark = pytest.mark.django_db


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
    assert respond.status_code == 200
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