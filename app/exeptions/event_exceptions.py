class EventError(Exception):
    """Base class for exceptions related with event"""
    pass

class EventValidationError(EventError):
    def __init__(self, description: str):
        super().__init__(f"Validation event error: {description}")

class EventQueryError(EventError):
    def __init__(self, description: str):
        super().__init__(f"Query error: {description}")