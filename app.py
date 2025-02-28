from flask import Flask, request, jsonify, send_from_directory
import redis
import json
import time
from config import redis_client
from auth import validate_api_key, generate_api_key, get_api_role, log_api_request

app = Flask(__name__, static_url_path='', static_folder='static')

# 🔹 Middleware: Require API Key for Protected Routes
@app.before_request
def require_api_key():
    """Validates API key before processing any request (except key generation & UI access)."""
    if request.endpoint not in ["generate_key", "serve_ui", "static"]:
        api_key = request.headers.get("X-API-Key")
        if not api_key or not validate_api_key(api_key):
            return jsonify({"error": "Unauthorized. Invalid API Key"}), 401

        # Log API Request
        log_api_request(api_key, request.path)

# 🔹 Web UI Route (Serves `index.html`)
@app.route("/")
def serve_ui():
    """Serves the Web UI"""
    return send_from_directory("static", "index.html")

# 🔹 API Key Generation Route
@app.route("/generate_key", methods=["POST"])
def generate_key():
    """Generates an API key for a user."""
    data = request.get_json()
    user_id = data.get("user_id")
    role = data.get("role", "user")  # Default to user role

    if not user_id or role not in ["admin", "user"]:
        return jsonify({"error": "User ID is required and role must be 'admin' or 'user'"}), 400

    api_key = generate_api_key(user_id, role)
    return jsonify({"api_key": api_key, "role": role}), 200

# ===================== API LOGGING & ADMIN FEATURES =====================

@app.route("/logs", methods=["GET"])
def get_api_logs():
    """Retrieve the last 50 API request logs (Admin only)."""
    api_key = request.headers.get("X-API-Key")
    
    # 🔹 Ensure the API Key belongs to an Admin
    if get_api_role(api_key) != "admin":
        return jsonify({"error": "Forbidden. Admin access required"}), 403

    # 🔹 Fetch last 50 API logs from Redis
    logs = redis_client.lrange("api_logs", -50, -1)
    logs = [json.loads(log) for log in logs] if logs else []

    return jsonify({"logs": logs}), 200

# ===================== BASIC REDIS OPERATIONS =====================

@app.route("/set", methods=["POST"])
def set_key():
    """Sets a key-value pair in Redis with optional TTL."""
    data = request.get_json()
    key = data.get("key")
    value = data.get("value")
    ttl = data.get("ttl")

    if not key or not value:
        return jsonify({"error": "Key and value are required"}), 400

    if ttl is not None:
        redis_client.setex(key, ttl, value)
    else:
        redis_client.set(key, value)

    return jsonify({"message": f"Stored '{key}' successfully!"}), 200

@app.route("/get", methods=["GET"])
def get_key():
    """Retrieves a key's value from Redis."""
    key = request.args.get("key")

    if not key:
        return jsonify({"error": "Key is required"}), 400

    value = redis_client.get(key)
    return json.dumps({"key": key, "value": value}), 200, {"Content-Type": "application/json"} if value else jsonify({"error": "Key not found"}), 404

@app.route("/list_keys", methods=["GET"])
def list_keys():
    """Lists all keys stored in Redis."""
    keys = redis_client.keys("*")
    return jsonify({"keys": keys}), 200

@app.route("/delete", methods=["DELETE"])
def delete_key():
    """Deletes a key from Redis (Admin only)."""
    api_key = request.headers.get("X-API-Key")
    if get_api_role(api_key) != "admin":
        return jsonify({"error": "Forbidden. Admin access required"}), 403

    data = request.get_json()
    key = data.get("key")

    if redis_client.exists(key):
        redis_client.delete(key)
        return jsonify({"message": f"Deleted '{key}' successfully!"}), 200
    else:
        return jsonify({"error": "Key not found"}), 404

# ===================== TTL (Expiration) Management =====================

@app.route("/expire", methods=["POST"])
def set_expiration():
    """Sets an expiration time (TTL) for a key in Redis."""
    data = request.get_json()
    key = data.get("key")
    ttl = data.get("ttl")

    if redis_client.exists(key):
        redis_client.expire(key, ttl)
        return jsonify({"message": f"TTL set for '{key}' to {ttl} seconds"}), 200
    else:
        return jsonify({"error": "Key not found"}), 404

@app.route("/ttl", methods=["GET"])
def get_ttl():
    """Gets the remaining TTL of a key in Redis."""
    key = request.args.get("key")
    ttl = redis_client.ttl(key)

    return jsonify({"key": key, "ttl": ttl}) if ttl >= 0 else jsonify({"error": "No TTL set or key not found"}), 404

# ===================== ADVANCED REDIS FEATURES =====================

# 🔹 Increment & Decrement
@app.route("/incr", methods=["POST"])
def increment_key():
    """Increments a numeric value by 1."""
    data = request.get_json()
    key = data.get("key")

    new_value = redis_client.incr(key)
    return jsonify({"key": key, "value": new_value}), 200

@app.route("/decr", methods=["POST"])
def decrement_key():
    """Decrements a numeric value by 1."""
    data = request.get_json()
    key = data.get("key")

    new_value = redis_client.decr(key)
    return jsonify({"key": key, "value": new_value}), 200

# 🔹 Hash Storage (HSET & HGET)
@app.route("/hset", methods=["POST"])
def hset():
    """Sets a field in a Redis Hash."""
    data = request.get_json()
    hash_name = data.get("hash")
    field = data.get("field")
    value = data.get("value")

    redis_client.hset(hash_name, field, value)
    return jsonify({"message": f"Stored field '{field}' in hash '{hash_name}'"}), 200

@app.route("/hget", methods=["GET"])
def hget():
    """Retrieves a field from a Redis Hash."""
    hash_name = request.args.get("hash")
    field = request.args.get("field")

    value = redis_client.hget(hash_name, field)
    return jsonify({"hash": hash_name, "field": field, "value": value}) if value else jsonify({"error": "Field not found"}), 404

# 🔹 Queue System Using Redis Lists
@app.route("/enqueue", methods=["POST"])
def enqueue():
    """Adds an item to a queue (Redis List)."""
    data = request.get_json()
    queue_name = data.get("queue")
    value = data.get("value")

    redis_client.rpush(queue_name, value)
    return jsonify({"message": f"Enqueued '{value}' to queue '{queue_name}'"}), 200

@app.route("/dequeue", methods=["GET"])
def dequeue():
    """Removes and returns the first item from a queue (Redis List)."""
    queue_name = request.args.get("queue")

    value = redis_client.lpop(queue_name)
    return jsonify({"queue": queue_name, "value": value}) if value else jsonify({"error": "Queue is empty"}), 404

if __name__ == "__main__":
    app.run(debug=True)
