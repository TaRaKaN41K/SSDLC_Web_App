import pytest
from unittest.mock import patch
import bcrypt

from api.utils.password import hash_password, validate_password
from exceptions.custom_exceptions import InvalidPasswordError


def test_hash_password_returns_bytes_and_logs():
    with patch("api.utils.password.loggers") as mock_loggers:
        password = "mysecret"
        hashed = hash_password(password)

        assert isinstance(hashed, bytes)
        # Проверяем, что хэш действительно соответствует паролю
        assert bcrypt.checkpw(password.encode(), hashed)

        mock_loggers['auth'].info.assert_called_once_with("Пароль успешно захеширован.")


def test_validate_password_success_and_logs():
    with patch("api.utils.password.loggers") as mock_loggers:
        password = "mypassword"
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        result = validate_password(password, hashed)
        assert result is True

        mock_loggers['auth'].info.assert_called_once_with("Пароль успешно проверен и совпадает.")


def test_validate_password_failure_raises():
    password = "mypassword"
    wrong_password = "wrongpassword"
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    with pytest.raises(InvalidPasswordError) as excinfo:
        validate_password(wrong_password, hashed)

    assert "Wrong password" in str(excinfo.value)
