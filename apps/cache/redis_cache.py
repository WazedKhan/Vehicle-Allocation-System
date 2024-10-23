# apps/cache/redis_cache.py

import redis
import json
from bson import ObjectId

class RedisCache:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis_client = redis.Redis(host=host, port=port, db=db)

    def _serialize(self, value):
        """Convert ObjectId to string to make it JSON serializable."""
        if isinstance(value, dict):
            return {key: str(val) if isinstance(val, ObjectId) else val for key, val in value.items()}
        return value

    def _deserialize(self, value):
        """Convert string back to ObjectId if necessary."""
        if isinstance(value, dict):
            return {key: ObjectId(val) if ObjectId.is_valid(val) else val for key, val in value.items()}
        return value

    def get(self, key):
        """Retrieve a value from Redis using the key."""
        value = self.redis_client.get(key)
        if value:
            return self._deserialize(json.loads(value))  # Convert from JSON string to Python object
        return None

    def set(self, key, value, expiration=3600):
        """Store a value in Redis with an optional expiration time."""
        serialized_value = self._serialize(value)  # Ensure value is serializable
        self.redis_client.setex(key, expiration, json.dumps(serialized_value))

    def delete(self, key):
        """Delete a key from Redis."""
        self.redis_client.delete(key)
