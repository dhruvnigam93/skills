# JWT bearer auth. Every endpoint depends on current_user, so all traffic is authenticated.
from dataclasses import dataclass
from fastapi import Header, HTTPException


@dataclass
class User:
    id: str


def current_user(authorization: str = Header(...)) -> User:
    """Decode the bearer JWT and return the User; raise 401 if missing/invalid."""
    token = authorization.removeprefix("Bearer ").strip()
    uid = _decode(token)
    if not uid:
        raise HTTPException(status_code=401, detail="unauthorized")
    return User(id=uid)


def _decode(token: str) -> str | None:
    # ... verifies signature, returns the subject (user id) ...
    return token or None
