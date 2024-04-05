from contextlib import contextmanager
from pathlib import Path
import duckdb

__all__ = ["get_db", "insert_song"]

sql_files = Path("sql").glob("*.sql")
sql_statements = {p.name.replace(".sql", ""): p.read_text() for p in sql_files}


@contextmanager
def get_db():
    con = duckdb.connect(database="duck.db", read_only=False)
    try:
        yield con
    finally:
        con.close()


def insert_song(name: str, artists: list[str] | None = None) -> None:
    with get_db() as db:
        statement = sql_statements["insert_song"]
        db.execute(statement, [name, artists])


def main() -> None:
    with get_db() as db:
        db.execute(sql_statements["create_songs_table"])
        db.execute("CREATE SEQUENCE IF NOT EXISTS seq_songid START 1;")
        db.execute(sql_statements["create_spotify_table"])
        db.execute("CREATE SEQUENCE IF NOT EXISTS seq_spotifyid START 1;")


if __name__ == "__main__":
    main()
