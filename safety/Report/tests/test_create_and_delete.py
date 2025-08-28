import pytest

from django.urls import reverse
from django.contrib.messages import get_messages
from ..models import BaseReport


def _seed(client, user, n):
    """
    สร้าง BaseReport จริง ๆ ลง DB ด้วย ORM (ไม่ mock ใด ๆ)
    """
    client.force_login(user)
    created = [BaseReport.objects.create(title=f"Flow Report #{i+1}") for i in range(n)]
    return created


def _delete_each_and_check(client, created_subset):
    """
    ลบแต่ละตัวผ่าน endpoint ลบ แล้วเช็ค redirect / ถูกลบ / มี message
    """
    for r in created_subset:
        delete_url = reverse("report:delete", args=[r.pk])
        resp_delete = client.post(delete_url, follow=True)

        # redirect มาที่ list
        assert resp_delete.wsgi_request.path == reverse("report:safety-report.list")

        # ถูกลบจริง
        assert not BaseReport.objects.filter(pk=r.pk).exists()

        # มีข้อความแจ้งเตือนประกอบ
        msgs = [m.message for m in get_messages(resp_delete.wsgi_request)]
        assert any("ลบรายงาน" in m and r.title in m for m in msgs)


# ========== กรณีที่ 1: ลบครบ (ควรผ่าน) ==========
@pytest.mark.django_db
def test_create_many_then_delete_all(client, user):
    num = 3
    created = _seed(client, user, num)

    # ลบครบทุกตัว
    _delete_each_and_check(client, created)

    remaining = BaseReport.objects.filter(pk__in=[r.pk for r in created]).count()
    assert remaining == 0


# ========== กรณีที่ 2 (A): ลบไม่ครบ คาดว่าเหลือ 1 ==========
@pytest.mark.django_db
def test_create_many_but_delete_incomplete_expect_left_1(client, user):
    num = 3
    created = _seed(client, user, num)

    # ลบแค่ 2 อันแรก (เหลือ 1)
    _delete_each_and_check(client, created[:-1])

    remaining = BaseReport.objects.filter(pk__in=[r.pk for r in created]).count()
    assert remaining == 1, f"คาดว่าเหลือ 1 แต่เหลือ {remaining}"


# ========== กรณีที่ 2 (B): negative test ด้วย xfail ==========
@pytest.mark.django_db
@pytest.mark.xfail(reason="จงใจลบไม่ครบ เพื่อตรวจว่าถ้าเหลืออยู่ ระบบจะจับ assertion ไม่เท่ากับ 0 ได้")
def test_create_many_but_delete_incomplete_xfail(client, user):
    num = 3
    created = _seed(client, user, num)

    # ลบแค่ 2 อันแรก (เหลือ 1)
    _delete_each_and_check(client, created[:-1])

    remaining = BaseReport.objects.filter(pk__in=[r.pk for r in created]).count()
    # ตั้งใจให้ assert ผิด เพื่อให้ xfail
    assert remaining == 0
