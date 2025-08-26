from django.urls import reverse

import pytest

from ..models import (
    BaseReport, HazardReport, GroundReport, AviationReport,
    SafetyReport, SafetyReportAircraftSystem, SafetyReportFlightPhase, SafetyReportEvent
)
from ..choices import (
    ReportTypeChoices, ReportStatusChoices, DamageTypeChoices,
    MissionTypeChoices, ReportTypeChoices, InjuryTypeChoices
)
from safety.Data.models import (
    Event, Aircraft, AircraftSystem, FlightPhase, Location, GroundSafetyCategory
)


@pytest.mark.django_db
def test_base_report_creation(user, base_report):

    base_report.keyword.add("test", "report")

    assert base_report.title == 'Test Base Report'
    assert base_report.recorder == user
    assert base_report.status == ReportStatusChoices.DRAFT
    assert str(base_report) == base_report.title


@pytest.mark.django_db
def test_hazard_report_creation(user, affiliation, base_report, category1):

    hazard_report = HazardReport.objects.create(
        base_report=base_report,
        affiliation=affiliation,
        location='Area 51',
        category=category1,
        first_recommendation='Handle carefully',
        initial_action_taken='Notify supervisor',
        anonymous=False
    )
    assert hazard_report.location == 'Area 51'
    assert hazard_report.affiliation == affiliation
    assert hazard_report.category == category1
    assert hazard_report.anonymous is False


@pytest.mark.django_db
def test_ground_incident_report_creation(user, affiliation, base_report):
    category = GroundSafetyCategory.objects.create(order=2, name="Category 2")

    ground_incident = GroundReport.objects.create(
        base_report=base_report,
        affiliation=affiliation,
        location='Runway 3',
        category=category,
        anonymous=True
    )
    assert ground_incident.anonymous is True
    assert ground_incident.category.name == "Category 2"


@pytest.mark.django_db
def test_aviation_incident_report_creation(user, squadron, base_report):
    aircraft = Aircraft.objects.create(model="F-35", name="Lightning II")
    system1 = AircraftSystem.objects.create(name="Engine")
    system2 = AircraftSystem.objects.create(name="Navigation")
    phase1 = FlightPhase.objects.create(name="Landing")
    phase2 = FlightPhase.objects.create(name="Takeoff")

    aviation_report = AviationReport.objects.create(
        base_report=base_report,
        squadron=squadron,
        aircraft=aircraft,
        anonymous=False
    )
    aviation_report.system.set([system1, system2])
    aviation_report.flight_phase.set([phase1, phase2])

    assert aviation_report.aircraft == aircraft
    assert system1 in aviation_report.system.all()
    assert phase2 in aviation_report.flight_phase.all()


@pytest.mark.django_db
def test_safety_report_and_relationships(user, squadron, base_report):
    aircraft = Aircraft.objects.create(model="Boeing 737", name="Boeing 737-800")
    system = AircraftSystem.objects.create(name="Communication System")
    phase = FlightPhase.objects.create(name="Cruise")
    event = Event.objects.create(name="Engine Failure")
    location = Location.objects.create(
        name="Base Camp",
        region='01',  # use valid RegionChoices key
        is_airforce=True,
        latitude=10.0,
        longitude=20.0
    )

    safety_report = SafetyReport.objects.create(
        base_report=base_report,
        squadron=squadron,
        mission_type=MissionTypeChoices.AIR,
        report_type=ReportTypeChoices.INCIDENT,
        aircraft=aircraft,
        damage_level=DamageTypeChoices.MAJOR,
        injury_type=InjuryTypeChoices.SAFE,
        location=location,
        latitude=location.latitude,
        longitude=location.longitude
    )

    # Add many-to-many relationships using through models
    SafetyReportAircraftSystem.objects.create(
        safety_report=safety_report,
        aircraft_system=system
    )
    SafetyReportFlightPhase.objects.create(
        safety_report=safety_report,
        flight_phase=phase
    )
    SafetyReportEvent.objects.create(
        safety_report=safety_report,
        event=event
    )

    # Check string representation
    assert str(safety_report) == base_report.title
    # Check url resolution
    url = safety_report.get_absolute_url()
    assert url == reverse("report:safety-overviews.main-page", kwargs={"base_report_id": safety_report.pk})

    # Validate relationships exist
    assert system in safety_report.aircraft_system.all()
    assert phase in safety_report.flight_phase.all()
    assert event in safety_report.event.all()
