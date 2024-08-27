from sqlalchemy.orm import Mapped

from app.db.base_model import Base


class System(Base):
    __tablename__= "systems"

    title: Mapped[str]