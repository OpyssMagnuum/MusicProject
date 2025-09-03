from pydantic import BaseModel, ConfigDict


class ArtistBase(BaseModel):
    name: str
    description: str


class ArtistCreate(ArtistBase):
    pass


class ArtistSchema(ArtistBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
