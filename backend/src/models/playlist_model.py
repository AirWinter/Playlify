from ..utils import chunks
from ..api import get_user_playlists_call, get_user_call, create_playlist_call, change_playlist_details_call, \
    add_songs_to_playlist_call


async def get_playlists(token: str):
    """
    Function to get all the user's playlist.
    :param token: User's access token
    :return: All the user's playlists
    """
    my_playlists = []
    count = 0
    while True:
        playlists = await get_user_playlists_call(token, limit=50, offset=count * 50)
        for playlist in playlists['items']:
            image = ''
            if len(playlist['images']) > 0:
                image = playlist['images'][0]['url']
            my_playlists.append(
                {"name": playlist['name'], "description": playlist['description'], "public": playlist['public'],
                 "imageUrl": image, 'link': playlist['external_urls']['spotify'],
                 'creator': playlist['owner']['display_name']})
        count += 1
        if len(playlists) < 50:
            break
    return my_playlists


async def create_playlist(token: str, name: str, song_ids: str, public: bool = False, description: str = None):
    """
    Function to create playlist
    :param token: User's access token
    :param name: Name of the playlist
    :param song_ids: Songs to populate the playlist with, comma separated string
    :param public: Optional boolean to indicate whether playlist should be public, default is false
    :param description: Optional description for the playlist
    """
    user = await get_user_call(token)
    # If the user provided a description
    if description is not None and description != "":
        response_create = await create_playlist_call(user_id=user['id'], token=token, name=name, public=public,
                                                     description=description)
        if 'description' not in response_create.keys() or response_create['description'] is None or response_create[
            'description'] == "":
            count = 0
            playlist_id = response_create['id']
            # Try at most 10 times to set the playlist description
            while count < 10:
                response_update = await change_playlist_details_call(playlist_id=playlist_id, token=token, name=name,
                                                                     description=description, public=public)
                count += 1
                if 'description' in response_update.keys() and response_update['description'] is not None and \
                        response_update['description'] != "":
                    break
    else:
        # Create empty playlist without a description
        response_create = await create_playlist_call(user_id=user['id'], token=token, name=name, public=public)

    playlist_id = response_create['id']
    songs_to_add = song_ids.split(",")

    # Populate Playlist
    for list_of_songs in chunks(songs_to_add, 100):
        await add_songs_to_playlist_call(playlist_id=playlist_id, token=token, track_ids=list_of_songs)
