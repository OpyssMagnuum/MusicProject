from sqlalchemy import Table, Column, Integer, ForeignKey

from src.database import Base

track_artist_association = Table(
    'track_artist',
    Base.metadata,
    Column('track_id', Integer, ForeignKey('tracks.id'), primary_key=True),
    Column('artist_id', Integer, ForeignKey('artists.id'), primary_key=True)
)
