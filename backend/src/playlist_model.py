from utils import chunks


def get_playlists(user_id, sp):
    """
    Function to get all the user's playlist.

    :param user_id: Spotify user id as a string
    :param sp: Connection to Spotify API to be able to recover the user's playlists
    :return: All of the user's playlists
    """
    my_playlists = []
    count = 0
    while True:
        playlists = sp.user_playlists(user=user_id, limit=50, offset=count * 50)
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


def create_playlist(user_id, req, sp):
    """
    Function to create and populate a playlist.

    :param user_id: Spotify user id as a string
    :param req: Request containing playlist name, description and songs to populate playlist with
    :param sp: Connection to Spotify API we call to create and populate playlist
    :return:
    """
    name = req['name']
    display_on_profile = False  # False by default
    # If public is specified then overwrite
    if 'display' in req.keys():
        display_on_profile = req['display']

    description = req['description']

    # If the user provided a description
    if description is not None and description != "":
        response_create = sp.user_playlist_create(user=user_id, name=name, public=display_on_profile,
                                                  description=description)
        if 'description' not in response_create.keys() or response_create['description'] is None or response_create[
            'description'] == "":
            count = 0
            playlist_id = response_create['id']
            # Try at most 10 times to set the playlist description
            while count < 10:
                response_update = sp.playlist_change_details(playlist_id=playlist_id, description=description)
                count += 1
                if 'description' in response_update.keys() and response_update['description'] is not None and \
                        response_update['description'] != "":
                    break
    else:
        # Create empty playlist without a description
        response_create = sp.user_playlist_create(user=user_id, name=name, public=display_on_profile)

    playlist_id = response_create['id']

    songs_to_add_string = req['songs_to_add']
    songs_to_add = songs_to_add_string.split(",")
    # print(f"Songs to add: {songs_to_add}")

    # Populate Playlist
    for list_of_songs in chunks(songs_to_add, 100):
        sp.playlist_add_items(playlist_id, list_of_songs)
        # print(f"Populated: {response_populate}")
