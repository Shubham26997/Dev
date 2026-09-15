from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine
import models
from router import auth, todos, admin

@asynccontextmanager
async def create_db_session(app: FastAPI):
    models.SQLModel.metadata.create_all(bind=engine) # will only run once and if the database is not created
    yield

app = FastAPI(lifespan=create_db_session, title="Udemy Tute")
app.include_router(admin.router, prefix="/admin", tags=['admin'])
app.include_router(auth.router, prefix="/auth", tags=['auth'])
app.include_router(todos.router, prefix="/todos", tags=['todos'])

