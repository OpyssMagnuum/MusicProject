from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.database import Base
from src.models.relationships import track_artist_association


class Artist(Base):
    __tablename__ = 'artists'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]

    tracks: Mapped[list["Track"]] = relationship(
        "Track",
        secondary=track_artist_association,
        back_populates="artists"
    )
