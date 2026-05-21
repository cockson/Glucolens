from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import settings
from urllib.parse import urlsplit


def get_rate_limit_key(request) -> str:
    # Trust forwarded headers from reverse proxies (Render/Nginx) first.
    forwarded_for = request.headers.get("x-forwarded-for", "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    real_ip = request.headers.get("x-real-ip", "").strip()
    if real_ip:
        return real_ip

    return get_remote_address(request)


# If Redis is not configured, use in-memory storage instead of an invalid empty URI.
def _storage_uri() -> str | None:
    url = (settings.REDIS_URL or "").strip()
    if not url:
        return "memory://"

    parsed = urlsplit(url)
    if settings.ENV == "prod" and parsed.hostname in {"localhost", "127.0.0.1", "::1"}:
        print("Rate limiter using memory storage because REDIS_URL points to localhost in production.")
        return "memory://"

    return url

limiter = Limiter(
    key_func=get_rate_limit_key,
    storage_uri=_storage_uri(),
    strategy="fixed-window",
    default_limits=[],
)
