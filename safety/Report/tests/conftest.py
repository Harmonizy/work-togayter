import os
import io
import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.utils import timezone

from ..choices import ReportTypeChoices, ReportStatusChoices, BaseReportTypeChoices
from ..models.reports import BaseReport
from ..models.attachments import Image, File, Recommendation
from tests.rtaf_user_fixtures import rank, affiliation, squadron, user
from ...Data.tests.conftest import category1, category2, aircraft, aircraft_boeing, aircraft_system1, aircraft_system2, aircraft_system_comm, flight_phase_landing, flight_phase_takeoff, flight_phase_cruise


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