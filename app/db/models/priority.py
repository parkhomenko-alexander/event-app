from sqlalchemy.orm import Mapped

from app.db.base_model import Base


class Priority(Base):
    __tablename__ = "priorities"
    
    title: Mapped[str]