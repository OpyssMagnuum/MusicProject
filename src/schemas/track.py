from pydantic import BaseModel, ConfigDict


class TrackOnlyAlbum(BaseModel):
    album_id: int | None = None


class TrackBase(TrackOnlyAlbum):
    name: str
    length: int
    genre: str
    year: int


class TrackCreate(TrackBase):
    pass


class TrackSchema(TrackBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
