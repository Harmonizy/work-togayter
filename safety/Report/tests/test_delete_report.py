# safety/Report/tests/test_delete_report.py
import pytest
from django.urls import reverse
from django.contrib.messages import get_messages

from ..models import BaseReport


@pytest.mark.django_db
def test_delete_report_post_deletes_and_redirects(client, user):
    # ใช้ฟิกซ์เจอร์ user จาก tests/rtaf_user_fixtures.py
    client.force_login(user)

    report = BaseReport.objects.create(title="Test Report")
    url = reverse("report:delete", args=[report.pk])

    resp = client.post(url, follow=True)

    # ถูกลบ
    assert not BaseReport.objects.filter(pk=report.pk).exists()
    # redirect ไปหน้า list
    assert resp.wsgi_request.path == reverse("report:safety-report.list")
    # มี success message
    msgs = [m.message for m in get_messages(resp.wsgi_request)]
    assert any("ลบรายงาน" in m and "Test Report" in m for m in msgs)


@pytest.mark.django_db
def test_delete_report_get_does_not_delete_and_redirects(client, user):
    client.force_login(user)

    report = BaseReport.objects.create(title="Still Here")
    url = reverse("report:delete", args=[report.pk])

    resp = client.get(url, follow=True)

    # ไม่ถูกลบ (GET)
    report.refresh_from_db()
    assert report.title == "Still Here"
    # redirect กลับ list
    assert resp.wsgi_request.path == reverse("report:safety-report.list")


@pytest.mark.django_db
def test_delete_report_404_when_pk_not_found(client, user):
    client.force_login(user)

    url = reverse("report:delete", args=[999999])

    r_get = client.get(url)
    assert r_get.status_code == 404

    r_post = client.post(url)
    assert r_post.status_code == 404
