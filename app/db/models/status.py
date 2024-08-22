from sqlalchemy.orm import Mapped

from app.db.base_model import Base


class Status(Base):
    __tablename__ = "statuses"
    
    title: Mapped[str]