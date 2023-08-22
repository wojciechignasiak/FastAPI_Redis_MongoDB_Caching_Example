class MongoDatabaseError(Exception):
    """Base exception for database related errors."""

class MongoNotFoundError(MongoDatabaseError):
    """Exception thrown when the record is not found."""
