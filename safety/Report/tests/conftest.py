import pytest


from ..choices import ReportTypeChoices, ReportStatusChoices, BaseReportTypeChoices, MissionTypeChoices
from ..models.reports import BaseReport

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