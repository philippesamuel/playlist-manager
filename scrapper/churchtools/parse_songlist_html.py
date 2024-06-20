from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
import click

FILE_PATH_DATE_FORMAT = r"%Y%m%d"
DATE_FORMAT = r"%Y-%m-%d"


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.argument
def main() -> None:
    file_path = Path("data/ct_agenda/html/20240616_songlist_de.html")
    date = parse_date_from_file_path(file_path=file_path)

    with file_path.open("r", encoding="utf-8") as file:
        content = file.read()

    songlist = parse_songlist(html_content=content)

    print(f"{date:{DATE_FORMAT}}")
    print(songlist)


def parse_songlist(html_content: str) -> list[dict]:
    soup = BeautifulSoup(html_content, "html.parser")

    # find songs in the html list
    song_nodes = soup.find_all("a", class_="select-song")
    return [parse_song_info(node) for node in song_nodes]


def parse_date_from_file_path(file_path: Path) -> datetime:
    file_name = file_path.name
    date_str, *_ = file_name.split("_")
    return datetime.strptime(date_str, FILE_PATH_DATE_FORMAT)


def parse_song_info(node) -> dict:
    return {
        "song_id": int(node["data-id"]),
        "song_name": node.text,
    }


if __name__ == "__main__":
    main()
