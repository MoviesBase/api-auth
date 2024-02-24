from urllib.parse import urlparse

from django.conf import settings
from redis.client import StrictRedis
from redlock import Redlock


def get_redis_client() -> StrictRedis:
    url_redis = urlparse(settings.REDIS_LOCATION)
    redis_kwargs = (
        {'ssl_cert_reqs': None} if url_redis.scheme == 'rediss' else {}
    )
    return StrictRedis.from_url(settings.REDIS_LOCATION, **redis_kwargs)


def get_lock_client(**kwargs) -> Redlock:
    return Redlock([get_redis_client()], **kwargs)
