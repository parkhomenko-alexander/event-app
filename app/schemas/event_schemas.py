from datetime import datetime

from app.schemas.general import BaseUserModel


class EventPostSchema(BaseUserModel):
    description: str

    priority_id: int
    system_id: int

class EventGetSchema(EventPostSchema):
    id: int

class EventFullyJoinedSchema(EventGetSchema):
    last_status: str
    creted_at: datetime
    updated_at: datetime
    priority: str
    system: str

class PaginatedEventsSchema(BaseUserModel):
    total_count: int
    filtered: int
    page: int
    per_page: int
    events: list[EventFullyJoinedSchema]