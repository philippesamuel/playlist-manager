from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import auth, user, song, artist

app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(song.router)
app.include_router(artist.router)

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://localhost:5500/frontend",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


def main():
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
