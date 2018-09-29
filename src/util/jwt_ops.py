import jwt
from time import time


def encode(payload: dict, secret: str, ttl: int) -> str:
    """
    Encodes the given payload with ttl and secret and returns it
    """
    payload["exp"] = int(time()) + (60 * ttl)
    return jwt.encode(payload, secret, algorithm='HS256').decode("utf-8")


def decode(encoded: str, secret: str) -> dict:
    """
    Decodes the payload with secret and returns the claims
    """
    return jwt.decode(encoded, secret, algorithms=['HS256'])