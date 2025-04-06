import redis
import logging
import os
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
        'version': '1.0.0',
        'environment': 'development'
    }
    
    # Check if we're in Railway environment
    if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RAILWAY_SERVICE_ID'):
        status['environment'] = 'railway'
        status['railway_service_id'] = os.environ.get('RAILWAY_SERVICE_ID', 'unknown')
    
    # Add Redis connection information
    status['redis_connection_info'] = {
        'redis_url': os.environ.get('REDIS_URL', 'Not set'),
        'database_url': os.environ.get('DATABASE_URL', 'Not set'),
        'redis_host': os.environ.get('REDIS_HOST', 'localhost'),
        'redis_port': os.environ.get('REDIS_PORT', '6379')
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
        
        # Add detailed environment information for troubleshooting
        if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RAILWAY_SERVICE_ID'):
            status['railway_debug_info'] = {
                'REDIS_URL': os.environ.get('REDIS_URL', 'Not set'),
                'DATABASE_URL': os.environ.get('DATABASE_URL', 'Not set'),
                'REDISHOST': os.environ.get('REDISHOST', 'Not set'),
                'REDIS_URI': os.environ.get('REDIS_URI', 'Not set'),
                'REDIS_HOST': os.environ.get('REDIS_HOST', 'Not set'),
                'REDIS_PORT': os.environ.get('REDIS_PORT', 'Not set')
            }
            logger.info("Added Railway debug information to health check response")
    except Exception as e:
        status['status'] = 'degraded'
        status['error'] = str(e)
        logger.error(f"Health check: Unexpected error - {str(e)}")
    
    return jsonify(status)