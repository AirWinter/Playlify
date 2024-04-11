from fastapi import APIRouter, Header, Response
from models.playlist_model import get_playlists, create_playlist
from typing import Annotated, Union
from pydantic import BaseModel

router = APIRouter(prefix='/playlist')


@router.api_route("/get-playlists", methods=['GET'])
async def get_playlists_endpoint(token: Annotated[str, Header()]):
    return await get_playlists(token)


class CreatePlaylistRequest(BaseModel):
    name: str
    songs_to_add: str
    display: bool = False
    description: Union[str, None] = None


@router.api_route("/create-playlist", methods=['POST'])
async def create_playlist_endpoints(token: Annotated[str, Header()], body: CreatePlaylistRequest):
    await create_playlist(token, body.name, body.songs_to_add, body.display, body.description)
    return Response(status_code=204)
