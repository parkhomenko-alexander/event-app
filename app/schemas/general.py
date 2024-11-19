from datetime import datetime
from typing import TypedDict

from fastapi import Query
from pydantic import AliasGenerator, BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel


class BaseUserModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=AliasGenerator(
            serialization_alias=to_camel,
        ),
        extra="ignore"
    )

class Pagination(BaseUserModel):
    per_page: int
    page: int