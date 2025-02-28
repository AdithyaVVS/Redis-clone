import secrets
import json
import time
from config import redis_client

API_KEY_PREFIX = "apikey:"  # Prefix for storing API keys in Redis
API_LOGS_KEY = "api_logs"   # Redis key for storing API logs

def generate_api_key(user_id, role="user"):
    """Generates and stores an API key for a user with a specified role (admin/user)."""
    api_key = secrets.token_hex(16)  # Generate a 32-character key
    redis_key = f"{API_KEY_PREFIX}{api_key}"

    # 🔹 Store user ID and role separately in Redis
    redis_client.hset(redis_key, "user_id", user_id)
    redis_client.hset(redis_key, "role", role)

    print(f"Generated API Key: {api_key} (Role: {role})")  # Debugging
    return api_key

def validate_api_key(api_key):
    """Checks if the API key is valid."""
    exists = redis_client.exists(f"{API_KEY_PREFIX}{api_key}")
    return exists

def get_api_role(api_key):
    """Retrieves the role associated with an API key (admin/user)."""
    return redis_client.hget(f"{API_KEY_PREFIX}{api_key}", "role")

def log_api_request(api_key, endpoint):
    """Logs API requests in Redis with a timestamp."""
    timestamp = int(time.time())  # Get current timestamp
    user_id = redis_client.hget(f"{API_KEY_PREFIX}{api_key}", "user_id")

    log_entry = {
        "user_id": user_id,
        "api_key": api_key,
        "endpoint": endpoint,
        "timestamp": timestamp
    }
    redis_client.rpush(API_LOGS_KEY, json.dumps(log_entry))  # Store log in Redis list
