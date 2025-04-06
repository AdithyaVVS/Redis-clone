import redis
import os
from urllib.parse import urlparse

# Connect to Redis
# Check for Railway's REDIS_URL first, then fall back to individual environment variables
redis_url = os.environ.get('REDIS_URL')

if redis_url:
    # Parse the Redis URL provided by Railway
    parsed_url = urlparse(redis_url)
    redis_host = parsed_url.hostname
    redis_port = parsed_url.port or 6379
    redis_password = parsed_url.password
else:
    # Fall back to individual environment variables or localhost for development
    redis_host = os.environ.get('REDIS_HOST', 'localhost')
    redis_port = int(os.environ.get('REDIS_PORT', 6379))
    redis_password = os.environ.get('REDIS_PASSWORD', None)

# Create Redis client with password if provided
if redis_password:
    redis_client = redis.StrictRedis(
        host=redis_host,
        port=redis_port,
        password=redis_password,
        decode_responses=True
    )
else:
    redis_client = redis.StrictRedis(
        host=redis_host,
        port=redis_port,
        decode_responses=True
    )
