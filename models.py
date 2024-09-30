from sqlmodel import SQLModel, Field
from pydantic import BaseModel, EmailStr

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)  # Added nullable=False
    email: str = Field(index=True, unique=True, nullable=False)      # Added nullable=False
    hashed_password: str = Field(nullable=False)                     # Added nullable=False


class UserCreate(BaseModel):
    username: str
    email: EmailStr  # This will validate email format
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True  # This allows reading from SQLModel instances
