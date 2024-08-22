from datetime import datetime
from typing import TypedDict

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class BaseUserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel, extra="ignore")

    id: int