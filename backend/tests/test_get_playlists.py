import unittest
import sample_data
from unittest.mock import MagicMock
from src.playlist_model import get_playlists


class TestGetPlaylists(unittest.TestCase):

    def test_get_playlists_returns_one_playlist(self):
        user_mock = {'id': 'abcdef'}
        sp_mock = MagicMock()
        sp_mock.user_playlists.return_value = sample_data.one_playlist_date

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
        sp_mock.user_playlists.return_value = sample_data.multiple_playlists_data

        actual = get_playlists(user_mock, sp_mock)

        self.assertEqual(4, len(actual))
