from pydantic import BaseModel, ConfigDict


class TrackBase(BaseModel):
    name: str
    length: int
    genre: str
    year: int
    album_id: int | None = None


class TrackCreate(TrackBase):
    pass


class TrackSchema(TrackBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
