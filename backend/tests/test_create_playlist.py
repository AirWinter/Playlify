import unittest
from src.playlist_model import create_playlist
from unittest.mock import MagicMock, call


class TestCreatePlaylist(unittest.TestCase):
    def test_create_playlist_empty_description(self):
        user_id = 'abcdef'
        req = {'display': False, 'description': "", 'songs_to_add': "abc,def", 'name': "Playlist Name"}
        sp_mock = MagicMock()
        sp_mock.user_playlist_create.return_value = {'id': "Playlist Id"}

        create_playlist(user_id, req, sp_mock)

        expected_calls = [call.user_playlist_create(user='abcdef', name='Playlist Name', public=False),
                          call.playlist_add_items('Playlist Id', ['abc', 'def'])]
        sp_mock.assert_has_calls(expected_calls)
        self.assertEqual(2, len(sp_mock.mock_calls))

    def test_create_playlist_with_description_no_retry(self):
        user_id = 'abcdef'
        req = {'display': True, 'description': "Playlist description", 'songs_to_add': "abc,def",
               'name': "Playlist Name"}
        sp_mock = MagicMock()
        sp_mock.user_playlist_create.return_value = {'id': "Playlist Id", 'description': "Playlist description"}

        create_playlist(user_id, req, sp_mock)

        expected_calls = [call.user_playlist_create(user='abcdef', name='Playlist Name', public=True,
                                                    description='Playlist description'),
                          call.playlist_add_items('Playlist Id', ['abc', 'def'])]
        sp_mock.assert_has_calls(expected_calls)
        self.assertEqual(2, len(sp_mock.mock_calls))

    def test_create_playlist_with_description_with_retry(self):
        user_id = 'abcdef'
        req = {'display': True, 'description': "Playlist description", 'songs_to_add': "abc,def",
               'name': "Playlist Name"}
        sp_mock = MagicMock()
        sp_mock.user_playlist_create.return_value = {'id': "Playlist Id"}
        sp_mock.playlist_change_details.return_value = {'id': "Playlist Id", 'description': "Playlist description"}

        create_playlist(user_id, req, sp_mock)

        expected_calls = [call.user_playlist_create(user='abcdef', name='Playlist Name', public=True,
                                                    description='Playlist description'),
                          call.playlist_change_details(playlist_id='Playlist Id', description='Playlist description'),
                          call.playlist_add_items('Playlist Id', ['abc', 'def'])]
        sp_mock.assert_has_calls(expected_calls)
        self.assertEqual(3, len(sp_mock.mock_calls))

    def test_create_playlist_with_description_max_retries(self):
        user_id = 'abcdef'
        req = {'display': True, 'description': "Playlist description", 'songs_to_add': "abc,def",
               'name': "Playlist Name"}
        sp_mock = MagicMock()
        sp_mock.user_playlist_create.return_value = {'id': "Playlist Id"}
        sp_mock.playlist_change_details.return_value = {'id': "Playlist Id"}

        create_playlist(user_id, req, sp_mock)

        expected_calls = [call.user_playlist_create(user='abcdef', name='Playlist Name', public=True,
                                                    description='Playlist description'),
                          call.playlist_change_details(playlist_id='Playlist Id', description='Playlist description'),
                          call.playlist_change_details(playlist_id='Playlist Id', description='Playlist description'),
                          call.playlist_change_details(playlist_id='Playlist Id', description='Playlist description'),
                          call.playlist_change_details(playlist_id='Playlist Id', description='Playlist description'),
                          call.playlist_change_details(playlist_id='Playlist Id', description='Playlist description'),
                          call.playlist_change_details(playlist_id='Playlist Id', description='Playlist description'),
                          call.playlist_change_details(playlist_id='Playlist Id', description='Playlist description'),
                          call.playlist_change_details(playlist_id='Playlist Id', description='Playlist description'),
                          call.playlist_change_details(playlist_id='Playlist Id', description='Playlist description'),
                          call.playlist_change_details(playlist_id='Playlist Id', description='Playlist description'),
                          call.playlist_add_items('Playlist Id', ['abc', 'def'])]
        sp_mock.assert_has_calls(expected_calls)
        self.assertEqual(12, len(sp_mock.mock_calls))
