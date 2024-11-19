from datetime import date, datetime

from pydantic import Field

from app.schemas.general import BaseUserModel


class RawEventInfoSchema(BaseUserModel):
    description: str

    priority: str
    system: str
    building_title: str
    room_title: str
    created_at: str

class EventPostSchema(BaseUserModel):
    description: str

    priority_id: int
    system_id: int

    building_id: int | None
    room_id: int | None


class EventGetSchema(EventPostSchema):
    id: int

class EventFullyJoinedSchema(EventGetSchema):
    last_status: str
    updated_at: datetime
    created_at: datetime
    priority: str
    system: str
    room: str | None
    building: str | None

class PaginatedEventsSchema(BaseUserModel):
    total_count: int
    filtered: int
    page: int
    per_page: int
    events: list[EventFullyJoinedSchema]

class EventsQueryFilters(BaseUserModel):
    sort_by: str
    sort_order: str