import unittest
from playlist_model import get_playlists
from unittest.mock import MagicMock


class TestGetPlaylists(unittest.TestCase):

    def test_get_playlists_returns_one_playlist(self):
        user_mock = {'id': 'abcdef'}
        sp_mock = MagicMock()
        sp_mock.user_playlists.return_value = {
            "href": "https://api.spotify.com/v1/users/i444vicbotfkqkh8un1x3sf75/playlists?offset=0&limit=50",
            "items": [
                {
                    "collaborative": 'false',
                    "description": "",
                    "external_urls": {
                        "spotify": "https://open.spotify.com/playlist/1v4IcpWhGEUiNwSthxAeV7"
                    },
                    "href": "https://api.spotify.com/v1/playlists/1v4IcpWhGEUiNwSthxAeV7",
                    "id": "1v4IcpWhGEUiNwSthxAeV7",
                    "images": [
                        {
                            "height": 640,
                            "url": "https://mosaic.scdn.co/640/ab67616d0000b2738f5636c9f7c8e432f81fe29aab67616d0000b273a496dc8c33ca6d10668b3157ab67616d0000b273cd733919ee57d0cc466e152fab67616d0000b273ef531a2218e0274cb4f67896",
                            "width": 640
                        },
                        {
                            "height": 300,
                            "url": "https://mosaic.scdn.co/300/ab67616d0000b2738f5636c9f7c8e432f81fe29aab67616d0000b273a496dc8c33ca6d10668b3157ab67616d0000b273cd733919ee57d0cc466e152fab67616d0000b273ef531a2218e0274cb4f67896",
                            "width": 300
                        },
                        {
                            "height": 60,
                            "url": "https://mosaic.scdn.co/60/ab67616d0000b2738f5636c9f7c8e432f81fe29aab67616d0000b273a496dc8c33ca6d10668b3157ab67616d0000b273cd733919ee57d0cc466e152fab67616d0000b273ef531a2218e0274cb4f67896",
                            "width": 60
                        }
                    ],
                    "name": "Test playlist",
                    "owner": {
                        "display_name": "AirWinter",
                        "external_urls": {
                            "spotify": "https://open.spotify.com/user/i444vicbotfkqkh8un1x3sf75"
                        },
                        "href": "https://api.spotify.com/v1/users/i444vicbotfkqkh8un1x3sf75",
                        "id": "i444vicbotfkqkh8un1x3sf75",
                        "type": "user",
                        "uri": "spotify:user:i444vicbotfkqkh8un1x3sf75"
                    },
                    "primary_color": 'null',
                    "public": 'false',
                    "snapshot_id": "NCwwOWYzYTM5Mzg2NjIyNjgyZDFkMjFlNzc1ZWY2ODk5NGY3OTdiNGNi",
                    "tracks": {
                        "href": "https://api.spotify.com/v1/playlists/1v4IcpWhGEUiNwSthxAeV7/tracks",
                        "total": 4
                    },
                    "type": "playlist",
                    "uri": "spotify:playlist:1v4IcpWhGEUiNwSthxAeV7"
                }
            ],
            "limit": 50,
            "next": 'null',
            "offset": 0,
            "previous": 'null',
            "total": 1
        }

        expected = [{
            "name": "Test playlist",
            "description": "",
            "public": 'false',
            "imageUrl": "https://mosaic.scdn.co/640/ab67616d0000b2738f5636c9f7c8e432f81fe29aab67616d0000b273a496dc8c33ca6d10668b3157ab67616d0000b273cd733919ee57d0cc466e152fab67616d0000b273ef531a2218e0274cb4f67896",
            "link": "https://open.spotify.com/playlist/1v4IcpWhGEUiNwSthxAeV7",
            "creator": "AirWinter"
        }]
        actual = get_playlists(user_mock, sp_mock)

        self.assertEqual(1, len(actual))
        self.assertEqual(expected, actual)

    def test_get_playlists_returns_multiple_playlists(self):
        user_mock = {'id': 'abcdef'}
        sp_mock = MagicMock()
        sp_mock.user_playlists.return_value = {
            "href": "https://api.spotify.com/v1/users/i444vicbotfkqkh8un1x3sf75/playlists?offset=0&limit=50",
            "items": [
                {
                    "collaborative": 'false',
                    "description": "",
                    "external_urls": {
                        "spotify": "https://open.spotify.com/playlist/1v4IcpWhGEUiNwSthxAeV7"
                    },
                    "href": "https://api.spotify.com/v1/playlists/1v4IcpWhGEUiNwSthxAeV7",
                    "id": "1v4IcpWhGEUiNwSthxAeV7",
                    "images": [
                        {
                            "height": 640,
                            "url": "https://mosaic.scdn.co/640/ab67616d0000b2738f5636c9f7c8e432f81fe29aab67616d0000b273a496dc8c33ca6d10668b3157ab67616d0000b273cd733919ee57d0cc466e152fab67616d0000b273ef531a2218e0274cb4f67896",
                            "width": 640
                        },
                        {
                            "height": 300,
                            "url": "https://mosaic.scdn.co/300/ab67616d0000b2738f5636c9f7c8e432f81fe29aab67616d0000b273a496dc8c33ca6d10668b3157ab67616d0000b273cd733919ee57d0cc466e152fab67616d0000b273ef531a2218e0274cb4f67896",
                            "width": 300
                        },
                        {
                            "height": 60,
                            "url": "https://mosaic.scdn.co/60/ab67616d0000b2738f5636c9f7c8e432f81fe29aab67616d0000b273a496dc8c33ca6d10668b3157ab67616d0000b273cd733919ee57d0cc466e152fab67616d0000b273ef531a2218e0274cb4f67896",
                            "width": 60
                        }
                    ],
                    "name": "Test playlist",
                    "owner": {
                        "display_name": "AirWinter",
                        "external_urls": {
                            "spotify": "https://open.spotify.com/user/i444vicbotfkqkh8un1x3sf75"
                        },
                        "href": "https://api.spotify.com/v1/users/i444vicbotfkqkh8un1x3sf75",
                        "id": "i444vicbotfkqkh8un1x3sf75",
                        "type": "user",
                        "uri": "spotify:user:i444vicbotfkqkh8un1x3sf75"
                    },
                    "primary_color": 'null',
                    "public": 'false',
                    "snapshot_id": "NCwwOWYzYTM5Mzg2NjIyNjgyZDFkMjFlNzc1ZWY2ODk5NGY3OTdiNGNi",
                    "tracks": {
                        "href": "https://api.spotify.com/v1/playlists/1v4IcpWhGEUiNwSthxAeV7/tracks",
                        "total": 4
                    },
                    "type": "playlist",
                    "uri": "spotify:playlist:1v4IcpWhGEUiNwSthxAeV7"
                },
                {
                    "collaborative": 'false',
                    "description": "",
                    "external_urls": {
                        "spotify": "https://open.spotify.com/playlist/2ekGXwrtuCXAo3rnNmoryn"
                    },
                    "href": "https://api.spotify.com/v1/playlists/2ekGXwrtuCXAo3rnNmoryn",
                    "id": "2ekGXwrtuCXAo3rnNmoryn",
                    "images": [],
                    "name": "My Playlist #3",
                    "owner": {
                        "display_name": "AirWinter",
                        "external_urls": {
                            "spotify": "https://open.spotify.com/user/i444vicbotfkqkh8un1x3sf75"
                        },
                        "href": "https://api.spotify.com/v1/users/i444vicbotfkqkh8un1x3sf75",
                        "id": "i444vicbotfkqkh8un1x3sf75",
                        "type": "user",
                        "uri": "spotify:user:i444vicbotfkqkh8un1x3sf75"
                    },
                    "primary_color": 'null',
                    "public": 'false',
                    "snapshot_id": "MSw5ZTc5NWQ2N2RiM2IxNDUyNjNkNTQ1OTQ3ZjU3NzFkMTU2YjRiMTE0",
                    "tracks": {
                        "href": "https://api.spotify.com/v1/playlists/2ekGXwrtuCXAo3rnNmoryn/tracks",
                        "total": 0
                    },
                    "type": "playlist",
                    "uri": "spotify:playlist:2ekGXwrtuCXAo3rnNmoryn"
                },
                {
                    "collaborative": 'false',
                    "description": "",
                    "external_urls": {
                        "spotify": "https://open.spotify.com/playlist/37i9dQZF1E8NYp4XFuIxzY"
                    },
                    "href": "https://api.spotify.com/v1/playlists/37i9dQZF1E8NYp4XFuIxzY",
                    "id": "37i9dQZF1E8NYp4XFuIxzY",
                    "images": [
                        {
                            "height": 'null',
                            "url": "https://seeded-session-images.scdn.co/v1/img/track/1BPBwKueIEMnUcbbs2te7B/en",
                            "width": 'null'
                        }
                    ],
                    "name": "NUMB Radio",
                    "owner": {
                        "display_name": "Spotify",
                        "external_urls": {
                            "spotify": "https://open.spotify.com/user/spotify"
                        },
                        "href": "https://api.spotify.com/v1/users/spotify",
                        "id": "spotify",
                        "type": "user",
                        "uri": "spotify:user:spotify"
                    },
                    "primary_color": 'null',
                    "public": 'false',
                    "snapshot_id": "MTY3Nzk0MjA5OSwwMDAwMDAwMDM2NWJhN2VkNzVkMjMyNGE2N2U0MDJmMWEzYmNjNjVm",
                    "tracks": {
                        "href": "https://api.spotify.com/v1/playlists/37i9dQZF1E8NYp4XFuIxzY/tracks",
                        "total": 50
                    },
                    "type": "playlist",
                    "uri": "spotify:playlist:37i9dQZF1E8NYp4XFuIxzY"
                },
                {
                    "collaborative": 'false',
                    "description": "These songs will get you motivated! The best playlist on Spotify for your Workouts (at home). Gym, Fitness , Cardio. Follow and get motivated \ud83d\udcaa\ud83c\udfc6",
                    "external_urls": {
                        "spotify": "https://open.spotify.com/playlist/2237sMNMlXS4wWLgdQ1UuV"
                    },
                    "href": "https://api.spotify.com/v1/playlists/2237sMNMlXS4wWLgdQ1UuV",
                    "id": "2237sMNMlXS4wWLgdQ1UuV",
                    "images": [
                        {
                            "height": 'null',
                            "url": "https://i.scdn.co/image/ab67706c0000bebbfe38c6a0037b742179aa6317",
                            "width": 'null'
                        }
                    ],
                    "name": "Workout Motivation 2023 \ud83d\udcaa",
                    "owner": {
                        "display_name": "Workout Music",
                        "external_urls": {
                            "spotify": "https://open.spotify.com/user/0m032eeptq5o63mbnwtfpybct"
                        },
                        "href": "https://api.spotify.com/v1/users/0m032eeptq5o63mbnwtfpybct",
                        "id": "0m032eeptq5o63mbnwtfpybct",
                        "type": "user",
                        "uri": "spotify:user:0m032eeptq5o63mbnwtfpybct"
                    },
                    "primary_color": 'null',
                    "public": 'false',
                    "snapshot_id": "MTMxNTcsYjEwOGZkMDc2Zjg1NmQyMmVkZmNmOTljZjAzYjQ0ODBlMTNlNzgxZg==",
                    "tracks": {
                        "href": "https://api.spotify.com/v1/playlists/2237sMNMlXS4wWLgdQ1UuV/tracks",
                        "total": 217
                    },
                    "type": "playlist",
                    "uri": "spotify:playlist:2237sMNMlXS4wWLgdQ1UuV"
                }
            ],
            "limit": 50,
            "next": 'null',
            "offset": 0,
            "previous": 'null',
            "total": 4
        }

        actual = get_playlists(user_mock, sp_mock)

        self.assertEqual(4, len(actual))
