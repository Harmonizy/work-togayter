import pytest

from safety.Data.models import (
    Event, Aircraft, AircraftSystem, FlightPhase, Location, GroundSafetyCategory
)

@pytest.fixture
def category1():
    return GroundSafetyCategory.objects.create(order=1, name="Category 1")


@pytest.fixture
def category2():
    return GroundSafetyCategory.objects.create(order=2, name="Category 2")


@pytest.fixture
def aircraft():
    return Aircraft.objects.create(model="F-35", name="Lightning II")


@pytest.fixture
def aircraft_boeing():
    return Aircraft.objects.create(model="Boeing 737", name="Boeing 737-800")


@pytest.fixture
def aircraft_system1():
    return AircraftSystem.objects.create(name="Engine")


@pytest.fixture
def aircraft_system2():
    return AircraftSystem.objects.create(name="Navigation")


@pytest.fixture
def aircraft_system_comm():
    return AircraftSystem.objects.create(name="Communication System")


@pytest.fixture
def flight_phase_landing():
    return FlightPhase.objects.create(name="Landing")


@pytest.fixture
def flight_phase_takeoff():
    return FlightPhase.objects.create(name="Takeoff")


@pytest.fixture
def flight_phase_cruise():
    return FlightPhase.objects.create(name="Cruise")


@pytest.fixture
def event_engine_failure():
    return Event.objects.create(name="Engine Failure")


@pytest.fixture
def location_base_camp():
    return Location.objects.create(
        name="Base Camp",
        region='01',  # Replace with valid RegionChoices key
        is_airforce=True,
        latitude=10.0,
        longitude=20.0
    )
