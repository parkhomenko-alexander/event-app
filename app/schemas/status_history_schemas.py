import datetime
from datetime import datetime

from app.schemas.general import BaseUserModel


class StstusHistoryPost(BaseUserModel):
    created_at: datetime
    
    status_id: int
    event_id: int
    user_id: int | None