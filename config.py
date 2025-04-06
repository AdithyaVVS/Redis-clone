import redis
import os
import time
import logging
from urllib.parse import urlparse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connect to Redis
# Check for Railway's REDIS_URL first, then fall back to individual environment variables
redis_url = os.environ.get('REDIS_URL')

if redis_url:
    # Parse the Redis URL provided by Railway
    logger.info(f"Using Redis URL from environment: {redis_url[:8]}...")
    parsed_url = urlparse(redis_url)
    redis_host = parsed_url.hostname
    redis_port = parsed_url.port or 6379
    redis_password = parsed_url.password
else:
    # Fall back to individual environment variables or localhost for development
    redis_host = os.environ.get('REDIS_HOST', 'localhost')
    redis_port = int(os.environ.get('REDIS_PORT', 6379))
    redis_password = os.environ.get('REDIS_PASSWORD', None)
    logger.info(f"Using Redis connection: {redis_host}:{redis_port}")

# Function to create Redis client with retry logic
def create_redis_client(max_retries=5, retry_delay=2):
    for attempt in range(max_retries):
        try:
            if redis_password:
                client = redis.StrictRedis(
                    host=redis_host,
                    port=redis_port,
                    password=redis_password,
                    decode_responses=True,
                    socket_timeout=5,
                    socket_connect_timeout=5
                )
            else:
                client = redis.StrictRedis(
                    host=redis_host,
                    port=redis_port,
                    decode_responses=True,
                    socket_timeout=5,
                    socket_connect_timeout=5
                )
            
            # Test the connection
            client.ping()
            logger.info("Successfully connected to Redis")
            return client
        except redis.exceptions.ConnectionError as e:
            logger.warning(f"Redis connection attempt {attempt+1}/{max_retries} failed: {str(e)}")
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error("Failed to connect to Redis after multiple attempts")
                # Return a client anyway, so the application can start and retry later
                if redis_password:
                    return redis.StrictRedis(
                        host=redis_host,
                        port=redis_port,
                        password=redis_password,
                        decode_responses=True
                    )
                else:
                    return redis.StrictRedis(
                        host=redis_host,
                        port=redis_port,
                        decode_responses=True
                    )

# Create Redis client with retry logic
redis_client = create_redis_client()
