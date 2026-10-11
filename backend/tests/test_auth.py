import time

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa

from app.core import auth
from app.core.config import settings

KEY = rsa.generate_private_key(public_exponent=65537, key_size=2048)


@pytest.fixture(autouse=True)
def local_signing_key(monkeypatch):
    # Stand in for Clerk's JWKS endpoint so tests never hit the network.
    signing_key = jwt.PyJWK.from_dict(
        {
            **jwt.algorithms.RSAAlgorithm.to_jwk(KEY.public_key(), as_dict=True),
            "alg": "RS256",
        }
    )
    monkeypatch.setattr(
        auth.jwks_client, "get_signing_key_from_jwt", lambda token: signing_key
    )


def make_token(key=KEY, **claims) -> str:
    payload = {
        "sub": "user_123",
        "iss": settings.clerk_issuer,
        "exp": int(time.time()) + 60,
        **claims,
    }
    return jwt.encode(payload, key, algorithm="RS256")


def get_with_token(client, token: str):
    return client.get("/admin/intakes", headers={"Authorization": f"Bearer {token}"})


def test_valid_token_is_accepted(client):
    assert get_with_token(client, make_token()).status_code == 200


def test_missing_token_is_rejected(client):
    assert client.get("/admin/intakes").status_code == 401


def test_malformed_token_is_rejected(client):
    assert get_with_token(client, "not-a-jwt").status_code == 401


def test_expired_token_is_rejected(client):
    assert (
        get_with_token(client, make_token(exp=int(time.time()) - 60)).status_code == 401
    )


def test_wrong_issuer_is_rejected(client):
    token = make_token(iss="https://someone-else.clerk.accounts.dev")
    assert get_with_token(client, token).status_code == 401


def test_token_signed_by_another_key_is_rejected(client):
    other_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    assert get_with_token(client, make_token(key=other_key)).status_code == 401
