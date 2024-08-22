from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import Base


class Event(Base):
    __tablename__ = "events"
    
    description: Mapped[str]

    status_id: Mapped[int] = mapped_column(ForeignKey("statuses.id"))
    priority_id: Mapped[int] = mapped_column(ForeignKey("priorities.id"))