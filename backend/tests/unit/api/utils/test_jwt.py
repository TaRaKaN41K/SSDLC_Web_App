import pytest
from unittest.mock import patch
from datetime import timedelta
import jwt

from api.utils.jwt import jwt_encode, jwt_decode, create_jwt
from exceptions.custom_exceptions import TokenExpiredError, InvalidTokenError, JWTEncodingError


@pytest.fixture
def payload():
    return {"sub": "user1"}


@pytest.fixture
def token():
    return "fake.jwt.token"


@pytest.mark.parametrize("expire_minutes, expire_timedelta", [
    (10, None),
    (None, timedelta(minutes=5)),
])
@patch("api.utils.jwt.jwt.encode", autospec=True)
@patch("api.utils.jwt.loggers")
def test_jwt_encode_success(mock_loggers, mock_jwt_encode, payload,
                            expire_minutes, expire_timedelta):
    mock_jwt_encode.return_value = "encoded_token"

    token = jwt_encode(payload, expire_minutes=expire_minutes or 10,
                       expire_timedelta=expire_timedelta)

    assert token == "encoded_token"
    mock_jwt_encode.assert_called_once()
    mock_loggers['auth'].info.assert_called_with(
        "JWT токен успешно закодирован")


@patch("api.utils.jwt.jwt.encode", side_effect=Exception("Encode error"), autospec=True)
def test_jwt_encode_failure(mock_jwt_encode, payload):
    with pytest.raises(JWTEncodingError) as excinfo:
        jwt_encode(payload)
    assert "Encode error" in str(excinfo.value)


@patch("api.utils.jwt.jwt.decode", autospec=True)
@patch("api.utils.jwt.loggers")
def test_jwt_decode_success(mock_loggers, mock_jwt_decode, token):
    mock_jwt_decode.return_value = {"sub": "user1"}
    result = jwt_decode(token)
    assert result == {"sub": "user1"}
    mock_jwt_decode.assert_called_once()
    mock_loggers['auth'].info.assert_called_with(
        "JWT токен успешно декодирован")


@patch("api.utils.jwt.jwt.decode", side_effect=jwt.ExpiredSignatureError, autospec=True)
def test_jwt_decode_expired_token(mock_jwt_decode, token):
    with pytest.raises(TokenExpiredError) as excinfo:
        jwt_decode(token)
    assert "expired" in str(excinfo.value).lower()


@patch("api.utils.jwt.jwt.decode", side_effect=jwt.InvalidTokenError("Invalid token"), autospec=True)
def test_jwt_decode_invalid_token(mock_jwt_decode, token):
    with pytest.raises(InvalidTokenError) as excinfo:
        jwt_decode(token)
    assert "invalid" in str(excinfo.value).lower()


@patch("api.utils.jwt.jwt_encode")
@patch("api.utils.jwt.loggers")
def test_create_jwt_calls_jwt_encode(mock_loggers, mock_jwt_encode):
    mock_jwt_encode.return_value = "new_token"
    data = {"user_id": 1}
    token_type = "access"

    token = create_jwt(token_type, data)

    assert token == "new_token"
    mock_jwt_encode.assert_called_once()

    call_args = mock_jwt_encode.call_args
    assert call_args is not None

    args, kwargs = call_args
    # Теперь payload скорее всего в kwargs:
    assert "payload" in kwargs, "payload не передан в jwt_encode"

    payload = kwargs["payload"]
    assert payload["type"] == token_type
    assert payload["user_id"] == 1

    mock_loggers['auth'].info.assert_called_with("JWT токен успешно создан")
