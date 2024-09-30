import os 
from sqlmodel import SQLModel, create_async_engine, AsyncSession
from dotenv import load_dotenv
from fastapi import Depends

# Load environment variables from .env file
load_dotenv()

# Get the database URL from environment variables
DATABASE_URL = os.getenv("postgresql+asyncpg://user:password@db:5432/user_db")
if DATABASE_URL is None:
    raise ValueError("DATABASE_URL environment variable not set")

# Create an asynchronous SQLAlchemy engine
engine = create_async_engine(DATABASE_URL, echo=True)  # Set echo=True for SQL logging during development

# Initialize the database
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Dependency to get a database session
async def get_session() -> AsyncSession:
    async with AsyncSession(engine) as session:
        yield session

