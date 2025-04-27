from exceptions.custom_exceptions import InvalidTokenType


def validate_token_type(
    payload: dict,
    token_type: str,
) -> bool:
    current_token_type = payload.get("type")
    if current_token_type != token_type:
        raise InvalidTokenType(f"Invalid token type {current_token_type} - expected {token_type}")
    return True
