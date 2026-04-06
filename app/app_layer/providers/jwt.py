from datetime import UTC, datetime

from jose import jwt


class JwtProvider:
    def __init__(self, secret: str, algo: str = "HS256", ttl_seconds: int = 86400) -> None:
        self._secret = secret
        self._algo = algo
        self._ttl_seconds = ttl_seconds

    def issue(self, sub: str) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": sub,
            "iat": now,
            "exp": now.timestamp() + self._ttl_seconds,
        }
        return jwt.encode(payload, self._secret, algorithm=self._algo)

    def decode(self, token: str) -> dict:
        return jwt.decode(token, self._secret, algorithms=[self._algo])
