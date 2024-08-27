from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import Base


class User(Base):
    __tablename__= "users"

    first_name: Mapped[str]
    last_name: Mapped[str]
    middle_name: Mapped[str]
    mail: Mapped[str] = mapped_column(unique=True)
    tz: Mapped[str]

