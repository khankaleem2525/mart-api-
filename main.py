from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, SQLModel
from database import init_db, engine, get_session  # Ensure get_session is imported
from models import User
from schemas import UserCreate, UserRead
from dependencies import get_password_hash, get_user, verify_password
from kafka_producer import send_message
from pydantic import BaseModel

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    init_db()

@app.post("/users/", response_model=UserRead)
async def create_user(user: UserCreate, session: Session = Depends(get_session)):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    
    session.add(db_user)
    await session.commit()  # Assuming this is an async session; adjust accordingly
    await session.refresh(db_user)
    
    # Send user data to Kafka
    send_message("user_created", user.dict())
    
    return db_user

@app.post("/login/")
async def login(username: str, password: str, session: Session = Depends(get_session)):
    user = await get_user(username, session)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    return {"msg": "Login successful", "user": user.username}

@app.get("/users/{user_id}", response_model=UserRead)
async def read_user(user_id: int, session: Session = Depends(get_session)):
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
