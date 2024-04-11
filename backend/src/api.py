import ssl
import aiohttp
import certifi
from aiohttp import ClientSession
from typing import List, Union
from utils import to_uri
import json

spotify_api = "https://api.spotify.com/v1"


async def get_user_playlists_call(token: str, offset: int, limit: int):
    url = spotify_api + "/me/playlists"
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': "application/json"
    }
    params = {'limit': limit,
              'offset': offset}
    return await api_get_call(url=url, headers=headers, params=params)


async def get_user_tracks_call(token: str, offset: int, limit: int):
    url = spotify_api + "/me/tracks"
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': "application/json"
    }
    params = {'limit': limit,
              'offset': offset}
    tracks = await api_get_call(url=url, headers=headers, params=params)
    return tracks['items']


async def get_artists_information_call(token: str, artist_ids: List[str]):
    url = spotify_api + "/artists"
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': "application/json"
    }
    ids = ",".join(artist_ids)
    params = {'ids': ids}
    return await api_get_call(url=url, headers=headers, params=params)


async def get_recommendations_call(token: str, seed_tracks: Union[List[str], None],
                                   seed_genres: Union[List[str], None], seed_artists: Union[List[str], None],
                                   limit: int):
    url = spotify_api + "/recommendations"
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': "application/json"
    }
    params = dict(limit=limit)
    if seed_genres:
        params['seed_genres'] = ','.join(seed_genres)

    if seed_artists:
        params['seed_artists'] = ','.join(seed_artists)

    if seed_tracks:
        params['seed_tracks'] = ','.join(seed_tracks)

    return await api_get_call(url=url, headers=headers, params=params)


async def get_user_call(token: str):
    url = f"{spotify_api}/me"
    headers = {
        'Authorization': f"Bearer {token}",
        'Content-Type': "application/json"
    }
    return await api_get_call(url=url, headers=headers)


async def create_playlist_call(user_id: str, token: str, name: str, description: Union[str, None] = None,
                               public: bool = False):
    url = f"{spotify_api}/users/{user_id}/playlists"
    headers = {
        'Authorization': f"Bearer {token}",
    }
    data = {'name': name, 'public': public}
    if description:
        data['description'] = description
    return await api_post_call(url, headers=headers, data=data)


async def change_playlist_details_call(playlist_id: str, token: str, name: str, description: Union[str, None] = None,
                                       public: bool = False):
    url = f"{spotify_api}/playlists/{playlist_id}"
    headers = {
        'Authorization': f"Bearer {token}",
    }
    data = {'name': name, 'public': public}
    if description:
        data['description'] = description
    return await api_put_call(url, headers=headers, data=data)


async def add_songs_to_playlist_call(playlist_id: str, token: str, track_ids: List[str]):
    url = f"{spotify_api}/playlists/{playlist_id}/tracks"
    headers = {
        'Authorization': f"Bearer {token}",
    }
    uris = [to_uri(track_id) for track_id in track_ids]
    data = {'uris': uris}
    return await api_post_call(url, headers=headers, data=data)


async def api_get_call(url, headers, params=None):
    ca_file = certifi.where()
    ssl_context = ssl.create_default_context(cafile=ca_file)
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    async with ClientSession(headers=headers, connector=connector) as session:
        async with session.get(url=url, params=params) as resp:
            return await resp.json()


async def api_post_call(url, headers, data):
    ca_file = certifi.where()
    ssl_context = ssl.create_default_context(cafile=ca_file)
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    async with ClientSession(headers=headers, connector=connector) as session:
        async with session.post(url=url, data=json.dumps(data)) as resp:
            return await resp.json()


async def api_put_call(url, headers, data):
    ca_file = certifi.where()
    ssl_context = ssl.create_default_context(cafile=ca_file)
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    async with ClientSession(headers=headers, connector=connector) as session:
        async with session.put(url=url, data=json.dumps(data)) as resp:
            return await resp.json()