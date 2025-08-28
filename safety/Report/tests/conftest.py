import os
import io
import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.utils import timezone

from ..choices import ReportTypeChoices, ReportStatusChoices, BaseReportTypeChoices, MissionTypeChoices
from ..models.reports import BaseReport
from ..models.attachments import Image, File, Recommendation
from tests.rtaf_user_fixtures import rank, affiliation, squadron, user
from ...Data.tests.conftest import category1, category2, aircraft, aircraft_boeing, aircraft_system1, aircraft_system2, aircraft_system_comm, flight_phase_landing, flight_phase_takeoff, flight_phase_cruise


@pytest.fixture
def base_report(user):
    br = BaseReport.objects.create(
        id=1,
        title='Test Base Report',
        description='Just a test',
        content='',
        recorder=user,
        status=ReportStatusChoices.DRAFT,
        report_type=BaseReportTypeChoices.SAFETY_GROUND,
        mission_type=MissionTypeChoices.AIR
    )
    br.keyword.add("test", "report")
    return br

@pytest.fixture
def media_root(tmp_path, settings):
    """
    ใช้ MEDIA_ROOT ชั่วคราวในแต่ละเทสเพื่อไม่ให้ไปปนกับสื่อจริง
    ใช้ร่วมกับ override_settings เพื่อให้ storage เขียนลง tmp_path
    """
    root = tmp_path / "test_media"
    root.mkdir(parents=True, exist_ok=True)
    with override_settings(MEDIA_ROOT=str(root)):
        yield str(root)


# ---------- BaseReport ----------
@pytest.fixture
def base_report(db, user):
    """
    สร้าง BaseReport แบบ minimal: กำหนดเฉพาะ title
    ฟิลด์อื่น ๆ ใช้ default ของโมเดลทั้งหมด
    """
    br = BaseReport.objects.create(
        title="รายงานทดสอบ",
        recorder=user,       # ไม่บังคับ แต่มีไว้ช่วยให้ทดสอบ logic ที่อิง user ได้
        anonymous=False,
        # ที่เหลือปล่อย default: fiscal_year, event_date, event_time, report_type, status, ...
    )
    return br


# ---------- Attachments ----------
@pytest.fixture
def uploaded_png():
    """
    ไฟล์ PNG เล็ก ๆ สำหรับอัปโหลดจำลอง
    """
    return SimpleUploadedFile(
        "pic.png",
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR",  # เฮดเดอร์ PNG
        content_type="image/png",
    )

@pytest.fixture
def uploaded_txt():
    """
    ไฟล์ข้อความเล็ก ๆ สำหรับอัปโหลดจำลอง
    """
    return SimpleUploadedFile(
        "doc.txt",
        b"hello world",
        content_type="text/plain",
    )


@pytest.fixture
def image_attachment(db, media_root, base_report, uploaded_png):
    """
    แนบ Image ให้ BaseReport ที่สร้างไว้
    """
    img = Image.objects.create(base_report=base_report, image=uploaded_png)
    # ตรวจสอบให้แน่ใจว่า storage เซฟแล้วและพาธถูก
    assert img.image.name
    return img


@pytest.fixture
def file_attachment(db, media_root, base_report, uploaded_txt):
    """
    แนบ File ให้ BaseReport ที่สร้างไว้
    """
    f = File.objects.create(base_report=base_report, file=uploaded_txt)
    assert f.file.name
    return f


@pytest.fixture
def recommendation_attachment(db, base_report):
    """
    แนบ Recommendation (ไม่มีไฟล์)
    """
    rec = Recommendation.objects.create(base_report=base_report, note="คำแนะนำเบื้องต้น")
    return rec

# -----------------------

@pytest.fixture
def base_form_minimal_fields(affiliation):
    return {
        "title": "รายงานใหม่",
        "priority": "LOW",
        "event_date": "2025-08-01",
        "event_time": "10:00:00",
        "affiliation": affiliation.pk if affiliation else "",
        "report_type": "S",
    }

@pytest.fixture
def empty_formsets_payload():
    return {
        "image-TOTAL_FORMS": "0",
        "image-INITIAL_FORMS": "0",
        "image-MIN_NUM_FORMS": "0",
        "image-MAX_NUM_FORMS": "1000",

        "recommendation-TOTAL_FORMS": "0",
        "recommendation-INITIAL_FORMS": "0",
        "recommendation-MIN_NUM_FORMS": "0",
        "recommendation-MAX_NUM_FORMS": "1000",

        "file-TOTAL_FORMS": "0",
        "file-INITIAL_FORMS": "0",
        "file-MIN_NUM_FORMS": "0",
        "file-MAX_NUM_FORMS": "1000",
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
        "title": "รายงานไม่ครบ",
        "priority": "INVALID",
        "event_date": "2025-08-01",
        "event_time": "10:00:00",
    }
    data.update(empty_formsets_payload)
    return data