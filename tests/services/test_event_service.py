
import pytest

from app.exeptions.event_exceptions import EventValidationError
from app.schemas.event_schemas import EventPostSchema, RawEventInfoSchema

# from app.schemas.event_schemas import EventPostSchema, RawEventInfoSchema


async def test_validate_event_success(
    main_mappings,
    event_service
):
    event = RawEventInfoSchema(
        description="погасли свечи",
        priority="Нормальный",
        system="mclim",
        building_title="Building A",
        room_title="Room 101",
        created_at="2024-09-27T07:00:00Z"
    )

    result: EventPostSchema | None = await event_service.validate_event(
        event=event,
        prior_mapping=main_mappings.priority_mapping,
        system_mapping=main_mappings.systems_mapping,
        building_mapping=main_mappings.buildings_mapping,
        room_mapping=main_mappings.rooms_mapping
    )

    assert result is not None
    assert result.priority_id == 1
    assert result.system_id == 1
    assert result.building_id == 101
    assert result.room_id == 201

@pytest.mark.asyncio
async def test_validate_event_priority_error(
    main_mappings,
    event_service
):
    event = RawEventInfoSchema(
        description="погасли свечи",
        priority="Нормальныйqqwe",
        system="mclim",
        building_title="Building A",
        room_title="Room 101",
        created_at="2024-09-27T07:00:00Z"
    )

    with pytest.raises(EventValidationError):
        await event_service.validate_event(
            event=event,
            prior_mapping=main_mappings.priority_mapping,
            system_mapping=main_mappings.systems_mapping,
            building_mapping=main_mappings.buildings_mapping,
            room_mapping=main_mappings.rooms_mapping
        )