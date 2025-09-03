from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.database import Base


class Album(Base):
    __tablename__ = 'albums'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    artist_id: Mapped[int]
    genre: Mapped[str]
    year: Mapped[int]

