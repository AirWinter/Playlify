import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import authentication_controller, tracks_controller, playlist_controller
import secrets

app = FastAPI()
app.include_router(authentication_controller.router)
app.include_router(tracks_controller.router)
app.include_router(playlist_controller.router)

origins = [
    secrets.url_base,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
