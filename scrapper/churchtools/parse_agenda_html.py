from pathlib import Path
from bs4 import BeautifulSoup

def main() -> None:
    file_path = Path("data/ct_agenda/html/20240616_agenda_de.html")
    # breakpoint()
    print(file_path.resolve())

    with file_path.open('r', encoding='utf-8') as file:
        content = file.read()
    soup = BeautifulSoup(content, "html.parser")

    # find songs in the html table
    attrs = ["data-song-id", "data-arrangement-id" ]
    for row in soup.find_all("a", class_="view-song"):
        song_info = {k: row[k] for k in attrs}
        name_raw = row.text
        name_parsed = ' '.join(name_raw.replace('\n', '').split())
        
        song_info.update({
            "name_raw": name_raw,
            "name_parsed": name_parsed
        })

        print(song_info)

def parse_raw_song_name(name_raw: str) -> str:
    removed_line_bread = name_raw.replace('\n', '')
    removed_multiple_spaces = ' '.join(removed_line_bread.split())
    return 
        



if __name__ == "__main__":
    main()
