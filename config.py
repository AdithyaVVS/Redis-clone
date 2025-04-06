import redis
import os

# Connect to Redis
# Use environment variables for production or default to localhost for development
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
