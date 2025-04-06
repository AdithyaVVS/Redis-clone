import redis
import logging
from flask import Blueprint, jsonify
from config import redis_client

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify application and Redis status"""
    status = {
        'status': 'ok',
        'redis_connected': False,
        'version': '1.0.0'
    }
    
    # Check Redis connection
    try:
        redis_info = redis_client.info()
        status['redis_connected'] = True
        status['redis_version'] = redis_info.get('redis_version', 'unknown')
        logger.info("Health check: Redis connection successful")
    except redis.exceptions.ConnectionError as e:
        status['status'] = 'degraded'
        status['redis_error'] = str(e)
        logger.error(f"Health check: Redis connection failed - {str(e)}")
    except Exception as e:
        status['status'] = 'degraded'
        status['error'] = str(e)
        logger.error(f"Health check: Unexpected error - {str(e)}")
    
    return jsonify(status)