import re
from datetime import datetime
from typing import Literal

from pydantic import Field, validator

from app.schemas.general import BaseUserModel


class EventPostSchema(BaseUserModel):
    description: str

    status_id: int
    priority_id: int