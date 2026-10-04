
from redis import Redis

from app.core.config import settings


redis_connection = Redis.from_url(
    settings.redis_url,
    decode_responses=True,
)
