from http.client import HTTPException
from typing import TypeVar
from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.schemas.album import AlbumSchema
from src.models.album import Album
from src.schemas.track import TrackSchema, TrackOnlyAlbum
from src.models.track import Track
from src.models.artist import Artist
from src.schemas.artist import ArtistSchema


from src.database import new_session

S = TypeVar('S', bound=BaseModel)
M = TypeVar('M')
Ar = TypeVar('Ar')
Br = TypeVar('Br')


async def try_commit(session: AsyncSession):
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(500, f'Database error: {str(e)}')


class BaseRepository:
    schema = type[S]
    model = type[M]

    @classmethod
    async def get_all(cls) -> list[S]:
        async with new_session() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return [cls.schema.model_validate(obj) for obj in result.scalars().all()]

    @classmethod
    async def add_one(cls, data: S) -> int:
        async with new_session() as session:
            dictionary = data.model_dump()
            res = cls.model(**dictionary)
            session.add(res)
            await session.flush()
            await try_commit(session)
            return res.id

    @classmethod
    async def get_one_by_id(cls, id: int) -> S:
        async with new_session() as session:
            query = select(cls.model).where(cls.model.id == id)
            result = await session.execute(query)
            obj = result.scalar_one_or_none()
            return cls.schema.model_validate(obj) if obj else None


class AssociationRepository:  # (Generic[Ar, Br, S]):
    schema: type[S]
    model_1: type[Ar]
    model_2: type[Br]
    relation_name: str  # задаём к кому отношение

    @classmethod
    async def add_association(cls, a_id: int, b_id: int) -> None:
        async with new_session() as session:
            obj_1 = await session.get(cls.model_1, a_id,
                                      options=[selectinload(getattr(cls.model_1, cls.relation_name))])
            obj_2 = await session.get(cls.model_2, b_id)

            if not obj_1 or not obj_2:
                raise HTTPException(404, "Object not found")

            relation = getattr(obj_1, cls.relation_name)
            if obj_2 not in relation:
                relation.append(obj_2)
                await try_commit(session)

    @classmethod
    async def get_associations(cls, a_id: int) -> list[S]:
        async with new_session() as session:
            query = select(cls.model_1).where(cls.model_1.id == a_id).options(
                selectinload(getattr(cls.model_1, cls.relation_name))
            )
            result = await session.execute(query)
            obj_1 = result.scalar_one_or_none()

            if not obj_1:
                raise HTTPException(404, "Object not found")

            relation = getattr(obj_1, cls.relation_name)
            return [cls.schema.model_validate(obj) for obj in relation]


class TrackRepository(BaseRepository):
    model = Track
    schema = TrackSchema

    @classmethod
    async def update_track_album(cls, id: int, data: TrackOnlyAlbum) -> dict:
        async with new_session() as session:
            new_data = data.model_dump()

            change = {'id': id, 'album_id': new_data.get('album_id')}
            stmt = (
                update(cls.model)
                .where(cls.model.id == change.get('id'))
                .values(album_id=change.get('album_id'))
            )
            await session.execute(stmt)
            await session.commit()
            return change


class ArtistRepository(BaseRepository):
    schema = ArtistSchema
    model = Artist


class AlbumRepository(BaseRepository):
    schema = AlbumSchema
    model = Album


class TrackArtistRepository(AssociationRepository):
    model_1 = Track
    model_2 = Artist
    schema = ArtistSchema
    relation_name = "artists"


class ArtistTrackRepository(AssociationRepository):
    model_1 = Artist
    model_2 = Track
    schema = TrackSchema
    relation_name = "tracks"
