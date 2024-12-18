from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Define the Base object for ORM models
Base = declarative_base()

# Create a global session factory
async_session_maker = None

class Database:
    _engine = None

    @classmethod
    def initialize(cls, database_url: str, echo: bool = False):
        """
        Initializes the async database engine and session factory.
        """
        global async_session_maker  # Use a global session maker
        cls._engine = create_async_engine(database_url, echo=echo, future=True)
        async_session_maker = sessionmaker(
            bind=cls._engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    @classmethod
    def get_session_factory(cls):
        """
        Returns the session factory.
        """
        if not async_session_maker:
            raise RuntimeError("Database not initialized!")
        return async_session_maker

    @classmethod
    async def close(cls):
        """
        Closes the async database engine.
        """
        if cls._engine:
            await cls._engine.dispose()
