from sqlmodel import Field, SQLModel, create_engine, Session
from typing import Annotated
from fastapi import Depends


class Fruit(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


if __name__ == "__main__":
    create_db_and_tables()
