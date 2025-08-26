import pytest
from django.urls import reverse, get_resolver
from rest_framework import status
from common.RTAFUser.models import RTAFUser

@pytest.fixture
def authenticated_client(client):
    test_user = RTAFUser.objects.create_user(username="testuser", password="password12345")
    assert test_user is not None, "Test user creation failed"
    logged_in = client.login(username="testuser", password="password12345")
    assert logged_in, "Client login failed"
    return client

@pytest.mark.django_db
@pytest.mark.parametrize(
    "url_name",
    [            
        ('login'),
        ('bs_view'),
        ('alpine'),
        ('htmx'),
        ('demo'),
        ('docx_example'),
        ('excel_example'),
    ],
)
def test_url_access(authenticated_client, url_name):
    url = reverse(url_name)
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK, f"URL '{url_name}' did not return 200 OK."

@pytest.mark.django_db
def test_authenticated_user_access(authenticated_client):
    url = reverse('RTAFUser:create')
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK, "Authenticated user could not access the create page."

@pytest.mark.django_db
def test_unauthenticated_user_redirect(client):
    url = reverse('RTAFUser:create')
    response = client.get(url)
    assert response.status_code == status.HTTP_302_FOUND, "Unauthenticated user was not redirected."
    assert "/login/" in response.url, "Unauthenticated user was not redirected to the login page."
