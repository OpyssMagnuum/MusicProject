from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from secret_stuff import db_conn_async


engine = create_async_engine(db_conn_async)
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_async_session() -> AsyncSession:
    async with new_session() as session:
        yield session

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
