CREATE TABLE IF NOT EXISTS spotify (
    id INTEGER PRIMARY KEY,
    song_id INTEGER,
    track_id VARCHAR(255),
    FOREIGN KEY(song_id) REFERENCES songs(id)
);