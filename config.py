import redis
import os
import time
import logging
from urllib.parse import urlparse

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connect to Redis
# Check for Railway's environment variables first, then fall back to local development settings

# Railway provides Redis URL in different formats depending on the plugin
# Try all possible environment variable names
redis_url = os.environ.get('REDIS_URL') or os.environ.get('REDISHOST') or os.environ.get('REDIS_URI')

if redis_url:
    # Parse the Redis URL provided by Railway
    # Only show beginning of URL in logs to avoid exposing credentials
    masked_url = f"{redis_url[:8]}..." if redis_url else "None"
    logger.info(f"Using Redis URL from environment: {masked_url}")
    
    try:
        parsed_url = urlparse(redis_url)
        redis_host = parsed_url.hostname
        redis_port = parsed_url.port or 6379
        redis_password = parsed_url.password
    except Exception as e:
        logger.error(f"Failed to parse Redis URL: {str(e)}")
        # Fallback to default values
        redis_host = 'localhost'
        redis_port = 6379
        redis_password = None
else:
    # Fall back to individual environment variables or localhost for development
    # Railway might provide these variables separately
    redis_host = os.environ.get('REDIS_HOST', 'localhost')
    redis_port = int(os.environ.get('REDIS_PORT', 6379))
    redis_password = os.environ.get('REDIS_PASSWORD', None)
    logger.info(f"Using Redis connection: {redis_host}:{redis_port}")

# Function to create Redis client with retry logic
def create_redis_client(max_retries=5, retry_delay=2):
    # For Railway deployment, we might need more retries as services start up
    if os.environ.get('RAILWAY_ENVIRONMENT'):
        max_retries = 10  # Increase retries for Railway environment
        retry_delay = 3   # Longer delay between retries
    
    for attempt in range(max_retries):
        try:
            # If we have a full Redis URL, use it directly
            if redis_url:
                client = redis.from_url(
                    redis_url,
                    decode_responses=True,
                    socket_timeout=5,
                    socket_connect_timeout=5
                )
            # Otherwise use individual connection parameters
            elif redis_password:
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
                # For Railway deployment, log additional information to help troubleshoot
                if os.environ.get('RAILWAY_ENVIRONMENT'):
                    logger.error(f"Railway deployment detected. Check if Redis plugin is properly configured.")
                    logger.error(f"Redis connection parameters: host={redis_host}, port={redis_port}")
                    logger.error(f"Environment variables: REDIS_URL={os.environ.get('REDIS_URL', 'Not set')}")
                
                # Return a client anyway, so the application can start and retry later
                # This allows the app to start and serve at least the health endpoint
                if redis_url:
                    return redis.from_url(redis_url, decode_responses=True)
                elif redis_password:
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
