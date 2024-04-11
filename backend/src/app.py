from dotenv import load_dotenv
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import authentication_controller, tracks_controller, playlist_controller

load_dotenv()

app = FastAPI()
app.secret_key = os.getenv("secret_key")
app.include_router(authentication_controller.router)
app.include_router(tracks_controller.router)
app.include_router(playlist_controller.router)

origins = [
    os.getenv("url_base")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=5000)
