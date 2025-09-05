from http.client import HTTPException
from typing import TypeVar

from fastapi import APIRouter
from pydantic import BaseModel

from src.repository import TrackRepository, ArtistRepository, AlbumRepository, TrackArtistRepository, \
    ArtistTrackRepository
from src.schemas.album import AlbumSchema, AlbumBase
from src.schemas.artist import ArtistSchema, ArtistBase
from src.schemas.relationships import TrackWithArtists, ArtistWithTracks
from src.schemas.track import TrackSchema, TrackBase, TrackOnlyAlbum

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


@router.patch('/tracks/{id}', tags=['Треки 🎧'], summary='Обновить альбом 🎚️')
async def update_track_album(id: int, data: TrackOnlyAlbum) -> dict:
    return await TrackRepository.update_track_album(id, data)


get_all_artists, add_artist = add_generic_routes(
    schema=ArtistSchema,
    base_schema=ArtistBase,
    repository=ArtistRepository,
    path='/artists',
    tags=['Артисты 👩‍🎤']
)

get_all_albums, add_album = add_generic_routes(
    schema=AlbumSchema,
    base_schema=AlbumBase,
    repository=AlbumRepository,
    path='/albums',
    tags=['Альбомы 🎷']
)


# RELATIONS

@router.post('/tracks/{track_id}/artists/{artist_id}',
             tags=['Треки-Артисты 🔗'],
             summary='Добавить артиста к треку 🎤')
async def add_artist_to_track(track_id: int, artist_id: int) -> dict:
    try:
        await TrackArtistRepository.add_association(track_id, artist_id)
        return {"ok": True, "message": "Artist added to track successfully"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"Error adding artist to track: {str(e)}")


@router.get('/tracks/{track_id}/artists',
            tags=['Треки-Артисты 🔗'],
            response_model=list[ArtistSchema],
            summary='Получить артистов трека 🎤')
async def get_track_artists(track_id: int) -> list[ArtistSchema]:
    try:
        return await TrackArtistRepository.get_associations(track_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"Error getting track artists: {str(e)}")


@router.get('/artists/{artist_id}/tracks',
            tags=['Треки-Артисты 🔗'],
            response_model=list[TrackSchema],
            summary='Получить треки артиста 🎵')
async def get_artist_tracks(artist_id: int) -> list[TrackSchema]:
    try:
        return await ArtistTrackRepository.get_associations(artist_id)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"Error getting artist tracks: {str(e)}")


@router.get('/tracks/{track_id}/with-artists',
            tags=['Треки-Артисты 🔗'],
            response_model=TrackWithArtists,
            summary='Получить трек с артистами 🎵🎤')
async def get_track_with_artists(track_id: int) -> TrackWithArtists:
    try:
        track = await TrackRepository.get_one_by_id(track_id)
        if not track:
            raise HTTPException(404, "Track not found")

        artists = await TrackArtistRepository.get_associations(track_id)

        track_dict = track.model_dump()
        track_dict['artists'] = artists

        return TrackWithArtists(**track_dict)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"Error getting track with artists: {str(e)}")


@router.get('/artists/{artist_id}/with-tracks',
            tags=['Треки-Артисты 🔗'],
            response_model=ArtistWithTracks,
            summary='Получить артиста с треками 👩‍🎤🎵')
async def get_artist_with_tracks(artist_id: int) -> ArtistWithTracks:
    try:
        artist = await ArtistRepository.get_one_by_id(artist_id)
        if not artist:
            raise HTTPException(404, "Artist not found")

        tracks = await ArtistTrackRepository.get_associations(artist_id)

        artist_dict = artist.model_dump()
        artist_dict['tracks'] = tracks

        return ArtistWithTracks(**artist_dict)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(500, f"Error getting artist with tracks: {str(e)}")

