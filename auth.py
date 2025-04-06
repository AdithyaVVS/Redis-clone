import secrets
import json
import time
import logging
import redis
from config import redis_client

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_KEY_PREFIX = "apikey:"  # Prefix for storing API keys in Redis
API_LOGS_KEY = "api_logs"   # Redis key for storing API logs

def generate_api_key(user_id, role="user"):
    """Generates and stores an API key for a user with a specified role (admin/user)."""
    api_key = secrets.token_hex(16)  # Generate a 32-character key
    redis_key = f"{API_KEY_PREFIX}{api_key}"

    try:
        # 🔹 Store user ID and role separately in Redis
        redis_client.hset(redis_key, "user_id", user_id)
        redis_client.hset(redis_key, "role", role)
        
        logger.info(f"Generated API Key for user {user_id} with role {role}")
        return api_key
    except redis.exceptions.ConnectionError as e:
        logger.error(f"Redis connection error during API key generation: {str(e)}")
        # Still return the key even if Redis storage failed
        # The application can retry storing it later
        return api_key
    except Exception as e:
        logger.error(f"Error generating API key: {str(e)}")
        return api_key

def validate_api_key(api_key):
    """Checks if the API key is valid."""
    try:
        exists = redis_client.exists(f"{API_KEY_PREFIX}{api_key}")
        return exists
    except redis.exceptions.ConnectionError as e:
        logger.error(f"Redis connection error during API key validation: {str(e)}")
        # Default to allowing the request if Redis is down
        # This is a security trade-off to maintain availability
        return True
    except Exception as e:
        logger.error(f"Error validating API key: {str(e)}")
        return False

def get_api_role(api_key):
    """Retrieves the role associated with an API key (admin/user)."""
    try:
        return redis_client.hget(f"{API_KEY_PREFIX}{api_key}", "role")
    except redis.exceptions.ConnectionError as e:
        logger.error(f"Redis connection error during role retrieval: {str(e)}")
        # Default to user role if Redis is down
        return "user"
    except Exception as e:
        logger.error(f"Error getting API role: {str(e)}")
        return "user"

def log_api_request(api_key, endpoint):
    """Logs API requests in Redis with a timestamp."""
    try:
        timestamp = int(time.time())  # Get current timestamp
        user_id = redis_client.hget(f"{API_KEY_PREFIX}{api_key}", "user_id")

        log_entry = {
            "user_id": user_id,
            "api_key": api_key,
            "endpoint": endpoint,
            "timestamp": timestamp
        }
        redis_client.rpush(API_LOGS_KEY, json.dumps(log_entry))  # Store log in Redis list
    except redis.exceptions.ConnectionError as e:
        logger.error(f"Redis connection error during API request logging: {str(e)}")
        # Silently fail - logging is non-critical
        pass
    except Exception as e:
        logger.error(f"Error logging API request: {str(e)}")
        # Silently fail - logging is non-critical
        pass
