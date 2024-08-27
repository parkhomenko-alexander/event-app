from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import Base


class StatusHistory(Base):
    __tablename__ = "statuses_history"

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True)
    )
    
    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"))
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))