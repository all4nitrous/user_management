from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Define the Base object
Base = declarative_base()

class Database:
    _engine = None
    _session_factory = None

    @classmethod
    def initialize(cls, database_url: str, echo: bool = False):
        """
        Initializes the async database engine and session factory.
        """
        cls._engine = create_async_engine(database_url, echo=echo, future=True)
        cls._session_factory = sessionmaker(
            bind=cls._engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    @classmethod
    def get_session(cls) -> AsyncSession:
        """
        Returns a new async session.
        """
        if not cls._session_factory:
            raise RuntimeError("Database not initialized!")
        return cls._session_factory()

    @classmethod
    async def close(cls):
        """
        Closes the async database engine.
        """
        if cls._engine:
            await cls._engine.dispose()
