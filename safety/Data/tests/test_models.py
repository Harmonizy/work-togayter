import pytest

from ..models import Event, Aircraft, AircraftSystem, FlightPhase, Location, GroundSafetyCategory
from ..choices import RegionChoices


@pytest.mark.django_db
def test_event_creation():
    event = Event.objects.create(name="Test Event")
    assert event.name == "Test Event"
    assert str(event) == "Test Event"


@pytest.mark.django_db
def test_aircraft_creation():
    aircraft = Aircraft.objects.create(model="F-16", name="F-16 Fighting Falcon")
    assert aircraft.model == "F-16"
    assert aircraft.name == "F-16 Fighting Falcon"
    assert str(aircraft) == "F-16 Fighting Falcon"


@pytest.mark.django_db
def test_aircraft_system_creation():
    system = AircraftSystem.objects.create(name="Navigation System")
    assert system.name == "Navigation System"
    assert str(system) == "Navigation System"


@pytest.mark.django_db
def test_flight_phase_creation():
    phase = FlightPhase.objects.create(name="Takeoff")
    assert phase.name == "Takeoff"
    assert str(phase) == "Takeoff"


@pytest.mark.django_db
def test_location_creation():
    location = Location.objects.create(
        name="Bangkok",
        region=RegionChoices.CENTRAL,  # Use first choice key
        is_airforce=True,
        latitude=13.7563,
        longitude=100.5018
    )
    assert location.name == "Bangkok"
    assert location.region == RegionChoices.CENTRAL
    assert location.is_airforce is True
    assert location.latitude == 13.7563
    assert location.longitude == 100.5018
    assert str(location) == "Bangkok"


@pytest.mark.django_db
def test_ground_safety_category_creation():
    category = GroundSafetyCategory.objects.create(order=1, name="Category A")
    assert category.order == 1
    assert category.name == "Category A"
    assert str(category) == "Category A"
