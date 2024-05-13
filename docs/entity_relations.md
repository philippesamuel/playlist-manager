Entities modeled in this project:

```mermaid
erDiagram

"YOUTUBE PLAYLIST" ||--|{ "YOUTUBE SONG": contains 
"CT WORSHIP SONGLIST" ||--|{ "CT SONG": contains
"CT SONG" ||--o{ "SPOTIFY TRACK": correspongs
"CT SONG" ||--o{ "YOUTUBE SONG": correspongs
"SPOTIFY PLAYLIST" ||--|{ "SPOTIFY TRACK": contains
"SPOTIFY TRACK" ||--|{ "SPOTIFY ARTIST": has

"CT WORSHIP SONGLIST" {
    date serviceDate
    string language
}

"CT SONG" {
    int id
    int CCLINumber
    str name
    List~str~ artistNames
}

"SPOTIFY PLAYLIST" {
    base62 id
    str name
}

"SPOTIFY TRACK" {
    base62 id
    str name
}

"SPOTIFY ARTIST" {
    base62 id
    str name
}

```