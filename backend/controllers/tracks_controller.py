from fastapi import APIRouter, Header, Request
from models.track_model import get_all_tracks_from_library, get_tracks_to_add, get_recommendations
from typing import Annotated, Union
from pydantic import BaseModel
import json

router = APIRouter(prefix='/tracks')


@router.api_route("/get-all", methods=['GET'])
async def get_all_tracks_endpoint(token: Annotated[str, Header()]):
    return await get_all_tracks_from_library(token)


class SongsToAddRequest(BaseModel):
    genres: Union[str, None] = ""
    artists: Union[str, None] = ""
    created_after_month: Union[str, None] = ""
    created_before_month: Union[str, None] = ""
    all_my_songs: str
    all_my_artists: str


@router.api_route('/get-tracks-to-add', methods=['POST'])
def get_tracks_to_add_endpoint(request: SongsToAddRequest):
    filters = {"genres": request.genres,
               "artists": request.artists,
               "created_after_month": request.created_after_month,
               "created_before_month": request.created_before_month}

    all_my_songs = json.loads(request.all_my_songs)
    all_my_artists = json.loads(request.all_my_artists)

    result = get_tracks_to_add(filters, all_my_songs, all_my_artists)

    return result


@router.api_route('/recommendations', methods=['GET'])
async def get_recommendations_endpoint(token: Annotated[str, Header()], request: Request):
    result = await get_recommendations(token, request.query_params['track_seeds'],
                                       request.query_params['genre_seeds'], request.query_params['artist_seeds'])

    return result


