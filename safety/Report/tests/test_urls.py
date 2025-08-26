import pytest
from django.urls import reverse

@pytest.mark.django_db
@pytest.mark.parametrize("url_name, kwargs", [
    ('report:safety-main', {}),
    ('report:safety-report.list', {}),
    # ('report:safety-overviews.main-page', {'base_report_id': 1}),
    ('report:safety-create.new-report', {'report_type': 'G'}),
    ('report:word_export.safety_doc', {'pk': 1}),
])
def test_report_urls(client, url_name, kwargs, base_report):
    url = reverse(url_name, kwargs=kwargs)
    response = client.get(url)
    assert response.status_code in (200, 302), f"URL {url} returned {response.status_code}"
