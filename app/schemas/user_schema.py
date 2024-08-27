from app.schemas.general import BaseUserModel


class UserPostSchema(BaseUserModel):
    first_name: str
    last_name: str
    middle_name: str
    mail: str
    tz: str

class UserGetSchema(UserPostSchema):
    id: int