from app.schemas.general import BaseUserModel


class EventPostSchema(BaseUserModel):
    description: str

    priority_id: int
    system_id: int

class EventGetSchema(EventPostSchema):
    id: int

class EventFullyJoined(EventGetSchema):
    status: str
    priority: str
    system: str

class PaginatedEvents(BaseUserModel):
    total_count: int
    filtered: int
    page: int
    per_page: int
    events: list[EventFullyJoined]