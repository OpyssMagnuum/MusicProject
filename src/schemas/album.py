from pydantic import BaseModel, ConfigDict


class AlbumBase(BaseModel):
    name: str
    artist_id: int
    year: int
    genre: str


class AlbumCreate(AlbumBase):
    pass


class AlbumSchema(AlbumBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
