from dataclasses import dataclass
from unittest.mock import AsyncMock

import pytest

from app.services.event_service import EventService


@dataclass
class Mappings:
    priority_mapping: dict[str, int]
    status_mapping: dict[str, int]
    systems_mapping: dict[str, int]
    buildings_mapping: dict[str, int]
    rooms_mapping: dict[str, int]
    
@pytest.fixture(scope="function")
def main_mappings() -> Mappings:
    return Mappings(
        priority_mapping={"Нормальный": 1, "Критический": 2},
        status_mapping={"Новый": 1, "В работе": 2, "Исполнено": 3},
        systems_mapping={"mclim": 1, "transformer": 2, "amelia": 3, "lift": 4},
        buildings_mapping={"Building A": 101},
        rooms_mapping={"Room 101": 201},
    )

@pytest.fixture(scope="function")
def mock_repository_manager():
    return AsyncMock()

@pytest.fixture(scope="function")
def event_service(mock_repository_manager):
    return EventService(repository_manager=mock_repository_manager)

