from app.core.security import (
    create_access_token,
    decode_token,
    hash_password,
    verify_password,
)


def test_password_hashing():
    password = "telesentinel_secret"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False


def test_token_creation():

    expected_user_id = 123
    token = create_access_token(expected_user_id)

    payload = decode_token(token)
    received_user_id = int(payload["sub"])
    assert received_user_id == expected_user_id
    assert "exp" in payload
