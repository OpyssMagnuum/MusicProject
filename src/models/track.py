from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.database import Base
from src.models.relationships import track_artist_association


class Track(Base):
    __tablename__ = 'tracks'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    length: Mapped[int]
    genre: Mapped[str]
    year: Mapped[int]
    album_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('albums.id')#, nullable=True, use_alter=True
    )

    artists: Mapped[list["Artist"]] = relationship(
        "Artist",
        secondary=track_artist_association,
        back_populates="tracks"
    )
