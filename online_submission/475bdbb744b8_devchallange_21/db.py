import contextlib

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from config.constants import DB_URL


class DataBaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(autoflush=False,
                                                                     autocommit=False,
                                                                     bind=self._engine)

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception('Session maker is not initialized')
        session = self._session_maker()
        try:
            yield session
        except Exception as e:
            print(f'Error: {e}')
            await session.rollback()
        finally:
            await session.close()


sessionmanager = DataBaseSessionManager(DB_URL)


async def get_db():
    async with sessionmanager.session() as session:
        yield session
