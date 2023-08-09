class DatabaseError(Exception):
    """Base exception for database related errors."""

class ConnectionError(DatabaseError):
    """Exception thrown when there is a problem with the connection."""

class InsertionError(DatabaseError):
    """Exception thrown when there is a problem inserting data."""

class DuplicateError(DatabaseError):
    """Exception thrown when a duplicate occurs."""

class NotFoundError(DatabaseError):
    """Exception thrown when the record is not found."""
