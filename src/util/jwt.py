import jwt
import time


class Jwt:
    def __init__(self, secret: str, ttl: int):
        self.secret = secret
        self.ttl = int(ttl)

    def encode(self, payload: dict) -> str:
        """
        Encodes the given payload with ttl and secret and returns it
        """
        payload["exp"] = int(time.time()) + (60 * self.ttl)
        return jwt.encode(payload, self.secret, algorithm='HS256').decode("utf-8")

    def decode(self, encoded: str) -> dict:
        """
        Decodes the payload with secret and returns the claims
        """
        return jwt.decode(encoded, self.secret, algorithms=['HS256'])