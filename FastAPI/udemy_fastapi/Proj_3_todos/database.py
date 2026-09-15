from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, Session

from passlib.context import CryptContext

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_db():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]