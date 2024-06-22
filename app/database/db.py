from sqlalchemy import create_engine
from sqlmodel import Session, SQLModel, create_engine


def get_session():
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
    

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def main() -> None:
    create_db_and_tables()


if __name__ == "__main__":
    main()
