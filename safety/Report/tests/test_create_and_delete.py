# safety/Report/tests/test_create_and_delete.py
import pytest
from django.urls import reverse
from django.contrib.messages import get_messages
from ..models import BaseReport


def _seed_and_mock(client, user, mocker, n):
    client.force_login(user)
    print("ขั้นที่ 0: ล็อกอินเรียบร้อย ✅")

    # สร้างของจริงลง test DB
    created = [BaseReport.objects.create(title=f"Flow Report #{i+1}") for i in range(n)]

    # mock service หน้า new_report ให้ success และคืนอินสแตนซ์ตามลำดับ
    mocker.patch(
        "safety.Report.views.safety_create.create_new_report",
        side_effect=[(True, (None, None, None, None), r) for r in created],
    )
    print(f"ขั้นที่ 1: seed BaseReport {n} รายการ + mock create_new_report เรียบร้อย ✅")
    return created


def _simulate_create(client, num_reports):
    create_url = reverse("report:safety-create.new_report")
    for i in range(num_reports):
        resp = client.post(create_url, {"priority": "LOW"})
        assert resp.status_code == 302
        assert resp.url == reverse("report:safety-report.list")
        print(f"ขั้นที่ 2.{i+1}: POST new_report #{i+1} → redirect {resp.url} ✅")


def _delete_each_and_check(client, created_subset):
    for i, r in enumerate(created_subset, start=1):
        delete_url = reverse("report:delete", args=[r.pk])
        resp_delete = client.post(delete_url, follow=True)
        # redirect ถูกหน้า
        assert resp_delete.wsgi_request.path == reverse("report:safety-report.list")
        # ถูกลบจริง
        assert not BaseReport.objects.filter(pk=r.pk).exists()
        # มี message
        msgs = [m.message for m in get_messages(resp_delete.wsgi_request)]
        assert any("ลบรายงาน" in m and r.title in m for m in msgs)
        remaining = BaseReport.objects.filter(
            pk__in=[x.pk for x in created_subset]
        ).count()
        print(f"ขั้นที่ 4.{i}: ลบ {r.title} แล้ว → redirect list ✅ | เหลือในชุดนี้ {remaining} รายการ")


# ========== กรณีที่ 1: ลบครบ (ควรผ่าน) ==========
@pytest.mark.django_db
def test_create_many_then_delete_all(client, user, mocker):
    num = 3
    created = _seed_and_mock(client, user, mocker, num)
    _simulate_create(client, num)

    # ลบครบทุกตัว
    _delete_each_and_check(client, created)

    remaining = BaseReport.objects.filter(pk__in=[r.pk for r in created]).count()
    print(f"→ หลังลบครบ เหลือ {remaining} รายการ")
    assert remaining == 0


# ========== กรณีที่ 2 (A): ลบไม่ครบ แต่ assert ให้ “ผ่าน” โดยคาดว่าเหลือ 1 ==========
@pytest.mark.django_db
def test_create_many_but_delete_incomplete_expect_left_1(client, user, mocker):
    num = 3
    created = _seed_and_mock(client, user, mocker, num)
    _simulate_create(client, num)

    # ลบแค่ 2 อันแรก (เหลือ 1)
    _delete_each_and_check(client, created[:-1])

    remaining = BaseReport.objects.filter(pk__in=[r.pk for r in created]).count()
    left = list(
        BaseReport.objects.filter(pk__in=[r.pk for r in created]).values_list("id", "title")
    )
    print(f"→ หลังลบไม่ครบ เหลือ {remaining} รายการ | เหลือตัวไหน: {left}")
    assert remaining == 1, f"คาดว่าเหลือ 1 แต่เหลือ {remaining}"


# ========== กรณีที่ 2 (B): ลบไม่ครบ แต่ทำเป็น “negative test” ด้วย xfail ==========
@pytest.mark.django_db
@pytest.mark.xfail(reason="จงใจลบไม่ครบ เพื่อตรวจว่าถ้าเหลืออยู่ ระบบจะจับ assertion ไม่เท่ากับ 0 ได้")
def test_create_many_but_delete_incomplete_xfail(client, user, mocker):
    num = 3
    created = _seed_and_mock(client, user, mocker, num)
    _simulate_create(client, num)

    # ลบแค่ 2 อันแรก (เหลือ 1)
    _delete_each_and_check(client, created[:-1])

    remaining = BaseReport.objects.filter(pk__in=[r.pk for r in created]).count()
    print(f"→ (xfail) หลังลบไม่ครบ เหลือ {remaining} รายการ")
    # ตั้งใจให้ assert ผิด เพื่อให้ xfail
    assert remaining == 0
