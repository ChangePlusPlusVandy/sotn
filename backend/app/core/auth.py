from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import settings

# Fetches and caches Clerk's public signing keys; the network call happens on first use.
jwks_client = jwt.PyJWKClient(f"{settings.clerk_issuer}/.well-known/jwks.json")
bearer = HTTPBearer(auto_error=False)


def get_current_staff(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
) -> str:
    """Verify the Clerk session token and return the signed-in staff member's Clerk user ID.

    Any signed-in Clerk user counts as staff, so Clerk sign-ups must stay restricted
    (see README). Role and area scoping come with the staff table.
    """
    unauthorized = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if credentials is None:
        raise unauthorized
    token = credentials.credentials
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=settings.clerk_issuer,
            options={"require": ["exp", "sub"]},
        )
    except jwt.PyJWTError:
        raise unauthorized
    return claims["sub"]


CurrentStaff = Annotated[str, Depends(get_current_staff)]
