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
redis_url = os.environ.get('REDIS_URL') or os.environ.get('REDISHOST') or os.environ.get('REDIS_URI') or os.environ.get('DATABASE_URL')

# For Railway deployment, check if we're in Railway environment
if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RAILWAY_SERVICE_ID'):
    logger.info("Railway environment detected, prioritizing Railway Redis configuration")
    # Railway may provide Redis URL in DATABASE_URL for Redis plugin
    if not redis_url and os.environ.get('DATABASE_URL'):
        redis_url = os.environ.get('DATABASE_URL')
        logger.info("Using DATABASE_URL for Redis connection")

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
        
        # Additional validation for Railway deployment
        if not redis_host and os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RAILWAY_SERVICE_ID'):
            # Try to extract host:port format if URL parsing failed
            if ':' in redis_url:
                parts = redis_url.split(':')
                if len(parts) >= 2:
                    potential_host = parts[0]
                    potential_port = parts[1]
                    # Remove any non-numeric characters from port
                    potential_port = ''.join(c for c in potential_port if c.isdigit())
                    if potential_host and potential_port:
                        redis_host = potential_host
                        redis_port = int(potential_port)
                        logger.info(f"Extracted Redis host:port from URL: {redis_host}:{redis_port}")
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
    if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RAILWAY_SERVICE_ID'):
        max_retries = 20  # Increase retries for Railway environment
        retry_delay = 5   # Longer delay between retries for Railway
    
    for attempt in range(max_retries):
        try:
            # If we have a full Redis URL, use it directly
            if redis_url:
                # Ensure URL has proper protocol prefix
                if not redis_url.startswith('redis://') and not redis_url.startswith('rediss://'):
                    redis_url = 'redis://' + redis_url
                    logger.info("Added redis:// protocol prefix to Redis URL")
                
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
                if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RAILWAY_SERVICE_ID'):
                    logger.error(f"Railway deployment detected. Check if Redis plugin is properly configured.")
                    logger.error(f"Redis connection parameters: host={redis_host}, port={redis_port}")
                    # Log all environment variables that might contain Redis connection info
                    logger.error(f"Environment variables:")
                    logger.error(f"  REDIS_URL={os.environ.get('REDIS_URL', 'Not set')}")
                    logger.error(f"  DATABASE_URL={os.environ.get('DATABASE_URL', 'Not set')}")
                    logger.error(f"  REDISHOST={os.environ.get('REDISHOST', 'Not set')}")
                    logger.error(f"  REDIS_URI={os.environ.get('REDIS_URI', 'Not set')}")
                    logger.error(f"  REDIS_HOST={os.environ.get('REDIS_HOST', 'Not set')}")
                    logger.error(f"  REDIS_PORT={os.environ.get('REDIS_PORT', 'Not set')}")
                    logger.error(f"  REDIS_PASSWORD={os.environ.get('REDIS_PASSWORD', 'Not set') != 'Not set' and '***' or 'Not set'}")
                
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
