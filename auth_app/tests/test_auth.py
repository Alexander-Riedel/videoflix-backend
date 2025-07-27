"""
auth_app.tests
~~~~~~~~~~~~~~

Test suite for user authentication endpoints:
registration, activation, login, logout,
token refresh, password reset and password confirmation.
"""

import pytest
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        "email": "user@example.com",
        "password": "securepassword",
        "confirmed_password": "securepassword"
    }


@pytest.fixture
def inactive_user():
    return User.objects.create_user(
        username="user@example.com",
        email="user@example.com",
        password="securepassword",
        is_active=False
    )


@pytest.fixture
def active_user():
    return User.objects.create_user(
        username="active@example.com",
        email="active@example.com",
        password="securepassword",
        is_active=True
    )


def test_register_user(api_client, user_data):
    response = api_client.post("/api/register/", user_data)
    assert response.status_code == 201
    assert response.data["user"]["email"] == user_data["email"]
    assert "token" in response.data


def test_activate_user(api_client, inactive_user):
    uidb64 = urlsafe_base64_encode(force_bytes(inactive_user.pk))
    token = default_token_generator.make_token(inactive_user)
    response = api_client.get(f"/api/activate/{uidb64}/{token}/")
    assert response.status_code == 200
    inactive_user.refresh_from_db()
    assert inactive_user.is_active is True


def test_login_success(api_client, active_user):
    response = api_client.post("/api/login/", {
        "email": active_user.email,
        "password": "securepassword"
    })
    assert response.status_code == 200
    assert response.data["user"]["username"] == active_user.username
    assert "access_token" in response.cookies
    assert "refresh_token" in response.cookies


def test_login_inactive_user(api_client, inactive_user):
    response = api_client.post("/api/login/", {
        "email": inactive_user.email,
        "password": "securepassword"
    })
    assert response.status_code == 400
    assert "detail" in response.data


def test_logout(api_client, active_user):
    login = api_client.post("/api/login/", {
        "email": active_user.email,
        "password": "securepassword"
    })
    api_client.cookies["refresh_token"] = login.cookies["refresh_token"].value
    api_client.cookies["access_token"] = login.cookies["access_token"].value
    api_client.force_authenticate(user=active_user)

    response = api_client.post("/api/logout/")
    assert response.status_code == 200
    assert "Refresh token is now invalid" in response.data["detail"]


def test_token_refresh(api_client, active_user):
    login = api_client.post("/api/login/", {
        "email": active_user.email,
        "password": "securepassword"
    })

    refresh_token = login.cookies.get("refresh_token")
    api_client.cookies["refresh_token"] = refresh_token.value

    response = api_client.post("/api/token/refresh/")
    assert response.status_code == 200
    assert "access" in response.data


def test_password_reset(api_client, active_user):
    response = api_client.post("/api/password_reset/", {
        "email": active_user.email
    })
    assert response.status_code == 200
    assert "reset your password" in response.data["detail"].lower()


def test_password_confirm(api_client, active_user):
    uidb64 = urlsafe_base64_encode(force_bytes(active_user.pk))
    token = default_token_generator.make_token(active_user)

    response = api_client.post(f"/api/password_confirm/{uidb64}/{token}/", {
        "new_password": "newsecurepassword",
        "confirm_password": "newsecurepassword"
    })
    assert response.status_code == 200
    assert "successfully reset" in response.data["detail"].lower()

    login = api_client.post("/api/login/", {
        "email": active_user.email,
        "password": "newsecurepassword"
    })
    assert login.status_code == 200
