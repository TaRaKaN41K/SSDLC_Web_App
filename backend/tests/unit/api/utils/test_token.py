import pytest
from unittest.mock import patch, MagicMock
from datetime import timedelta

from api.utils.token import create_access_token, create_refresh_token
from schemas import UserSchema
from config import settings


@pytest.fixture
def user():
    return UserSchema(
        id=1,
        name="testuser",
        email="test@example.com",
        password=b"fakepassword123",  # вот здесь байты
        photo_filename="photo.jpg"
    )


@patch("api.utils.token.create_jwt")
@patch("api.utils.token.loggers")
def test_create_access_token(mock_loggers, mock_create_jwt, user):
    mock_create_jwt.return_value = "access_token_mock"

    token = create_access_token(user)

    assert token == "access_token_mock"
    mock_create_jwt.assert_called_once_with(
        token_type="access",
        token_data={
            "sub": user.name,
            "username": user.name,
            "email": user.email,
        },
        expire_minutes=settings.auth_jwt.access_token_expire_minutes,
    )
    mock_loggers['auth'].info.assert_called_once_with(
        f"Создан access токен для пользователя {user.name}"
    )


@patch("api.utils.token.create_jwt")
@patch("api.utils.token.loggers")
def test_create_refresh_token(mock_loggers, mock_create_jwt, user):
    mock_create_jwt.return_value = "refresh_token_mock"

    token = create_refresh_token(user)

    assert token == "refresh_token_mock"
    mock_create_jwt.assert_called_once_with(
        token_type="refresh",
        token_data={
            "sub": user.name,
        },
        expire_timedelta=timedelta(days=settings.auth_jwt.refresh_token_expire_days),
    )
    mock_loggers['auth'].info.assert_called_once_with(
        f"Создан refresh токен для пользователя {user.name}"
    )
