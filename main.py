from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)

from contextlib import asynccontextmanager
from fastapi import FastAPI

from sqlmodel import SQLModel
from database import engine
from routes.users import router as users_router
from routes.tasks import router as tasks_router
import models  # type: ignore


@asynccontextmanager
async def lifespan(_: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


app.include_router(users_router)
app.include_router(tasks_router)
