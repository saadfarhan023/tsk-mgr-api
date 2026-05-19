from os import getenv
from sqlmodel import create_engine, Session

DATABASE_URL = getenv("DATABASE_URL")
if DATABASE_URL is None:
    print("DATABASE_URL env not found.")
    exit()

engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
