import pytest

from common.RTAFUser.models import RTAFUser, Affiliation, Squadron, Rank


@pytest.fixture
def rank():
    return Rank.objects.create(id=1, short_name="Sgt", is_airforce=True, level=5)


@pytest.fixture
def affiliation():
    return Affiliation.objects.create(short_name="BaseCamp", full_name="Base Camp", is_airbase=True)


@pytest.fixture
def squadron(affiliation):
    return Squadron.objects.create(code="SQ-X", affiliation=affiliation)


@pytest.fixture
def user(rank, affiliation):
    return RTAFUser.objects.create(username="testuser", rank=rank, affiliation=affiliation, work_affiliation=affiliation)
