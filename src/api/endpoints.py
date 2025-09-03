from typing import TypeVar

from fastapi import APIRouter
from pydantic import BaseModel

from src.repository import TrackRepository, ArtistRepository
from src.schemas.artist import ArtistSchema, ArtistBase
from src.schemas.track import TrackSchema, TrackBase

router = APIRouter()

S = TypeVar('S', bound=BaseModel)
SB = TypeVar('SB', bound=BaseModel)
M = TypeVar('M')
R = TypeVar('R')


def add_generic_routes(
        schema: type[S],
        base_schema: type[SB],
        repository: R,
        path: str,
        tags: list[str]
):
    # GET endpoint
    @router.get(path, tags=tags, summary=f"Получить все \"{tags[0]}\" 🎶")
    async def get_all() -> list[schema]:
        return await repository.get_all()

    # POST endpoint
    @router.post(path, tags=tags, summary=f"Добавить один в \"{tags[0]}\" 🎵")
    async def add_one(data: base_schema) -> dict:
        one_id = await repository.add_one(data)
        return {"ok": True, "id": one_id}

    return get_all, add_one


get_all_tracks, add_track = add_generic_routes(
    schema=TrackSchema,
    base_schema=TrackBase,
    repository=TrackRepository,
    path='/tracks',
    tags=['Треки 🎧']
)

get_all_artists, add_artist = add_generic_routes(
    schema=ArtistSchema,
    base_schema=ArtistBase,
    repository=ArtistRepository,
    path='/artists',
    tags=['Артисты 👩‍🎤']
)
