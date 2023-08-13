import unittest
import sample_data
from tracks_model import get_tracks_to_add
from unittest.mock import patch


class TestGetTracksToAdd(unittest.TestCase):

    @patch('mongodb_repository.get_by_user_id')
    def test_get_tracks_to_add_no_filters_returns_everything(self, repo):
        filters = {'artists': "", 'genres': "", 'created_after_month': "", 'created_before_month': ""}
        repo.return_value = sample_data.all_my_songs
        expected = {'song 1 id': {'artists': [{'external_url': 'url artist 1',
                                               'name': 'artist 1 name'}],
                                  'preview_url': 'song 1 preview_url',
                                  'song_name': 'Song 1 Name',
                                  'song_url': 'external_url song 1'},
                    'song 2 id': {'artists': [{'external_url': 'url artist 2',
                                               'name': 'artist 2 name'}],
                                  'preview_url': 'song 2 preview_url',
                                  'song_name': 'Song 2 Name',
                                  'song_url': 'external_url song 2'},
                    'song 3 id': {'artists': [{'external_url': 'url artist 3',
                                               'name': 'artist 3 name'}],
                                  'preview_url': 'song 3 preview_url',
                                  'song_name': 'Song 3 Name',
                                  'song_url': 'external_url song 3'}}
        actual = get_tracks_to_add(filters, "random id")
        self.assertEqual(expected, actual)

    @patch('mongodb_repository.get_by_user_id')
    def test_get_tracks_to_add_filter_by_any_genre_returns_everything(self, repo):
        filters = {'artists': "", 'genres': "some genre;any", 'created_after_month': "", 'created_before_month': ""}
        repo.return_value = sample_data.all_my_songs

        expected = {'song 1 id': {'artists': [{'external_url': 'url artist 1',
                                               'name': 'artist 1 name'}],
                                  'preview_url': 'song 1 preview_url',
                                  'song_name': 'Song 1 Name',
                                  'song_url': 'external_url song 1'},
                    'song 2 id': {'artists': [{'external_url': 'url artist 2',
                                               'name': 'artist 2 name'}],
                                  'preview_url': 'song 2 preview_url',
                                  'song_name': 'Song 2 Name',
                                  'song_url': 'external_url song 2'},
                    'song 3 id': {'artists': [{'external_url': 'url artist 3',
                                               'name': 'artist 3 name'}],
                                  'preview_url': 'song 3 preview_url',
                                  'song_name': 'Song 3 Name',
                                  'song_url': 'external_url song 3'}}
        actual = get_tracks_to_add(filters, "random user id")
        self.assertEqual(expected, actual)

    @patch('mongodb_repository.get_by_user_id')
    def test_get_tracks_to_add_filter_by_genre2_returns_two_songs(self, repo):
        filters = {'artists': "", 'genres': "genre 2", 'created_after_month': "", 'created_before_month': ""}
        repo.return_value = sample_data.all_my_songs

        expected = {'song 1 id': {'artists': [{'external_url': 'url artist 1',
                                               'name': 'artist 1 name'}],
                                  'preview_url': 'song 1 preview_url',
                                  'song_name': 'Song 1 Name',
                                  'song_url': 'external_url song 1'},
                    'song 2 id': {'artists': [{'external_url': 'url artist 2',
                                               'name': 'artist 2 name'}],
                                  'preview_url': 'song 2 preview_url',
                                  'song_name': 'Song 2 Name',
                                  'song_url': 'external_url song 2'}}
        actual = get_tracks_to_add(filters, "random user id")
        self.assertEqual(expected, actual)

    @patch('mongodb_repository.get_by_user_id')
    def test_get_tracks_to_add_filter_by_create_after_returns_song3(self, repo):
        filters = {'artists': "", 'genres': "", 'created_after_month': "2023-03-01", 'created_before_month': ""}
        repo.return_value = sample_data.all_my_songs

        expected = {'song 3 id': {'artists': [{'external_url': 'url artist 3',
                                               'name': 'artist 3 name'}],
                                  'preview_url': 'song 3 preview_url',
                                  'song_name': 'Song 3 Name',
                                  'song_url': 'external_url song 3'}}
        actual = get_tracks_to_add(filters, "random user id")
        self.assertEqual(expected, actual)

    @patch('mongodb_repository.get_by_user_id')
    def test_get_tracks_to_add_filter_by_artists(self, repo):
        filters = {'artists': "artist 1 id;artist 2 id", 'genres': "", 'created_after_month': "",
                   'created_before_month': ""}
        repo.return_value = sample_data.all_my_songs

        expected = {'song 1 id': {'artists': [{'external_url': 'url artist 1',
                                               'name': 'artist 1 name'}],
                                  'preview_url': 'song 1 preview_url',
                                  'song_name': 'Song 1 Name',
                                  'song_url': 'external_url song 1'},
                    'song 2 id': {'artists': [{'external_url': 'url artist 2',
                                               'name': 'artist 2 name'}],
                                  'preview_url': 'song 2 preview_url',
                                  'song_name': 'Song 2 Name',
                                  'song_url': 'external_url song 2'}}
        actual = get_tracks_to_add(filters, "random user id")
        self.assertEqual(expected, actual)

    @patch('mongodb_repository.get_by_user_id')
    def test_get_tracks_to_add_filter_by_artists_and_created_before_month(self, repo):
        filters = {'artists': "artist 1 id;artist 2 id", 'genres': "", 'created_after_month': "",
                   'created_before_month': "2023-01-31"}
        repo.return_value = sample_data.all_my_songs

        expected = {'song 1 id': {'artists': [{'external_url': 'url artist 1',
                                               'name': 'artist 1 name'}],
                                  'preview_url': 'song 1 preview_url',
                                  'song_name': 'Song 1 Name',
                                  'song_url': 'external_url song 1'},
                    }
        actual = get_tracks_to_add(filters, "random user id")
        self.assertEqual(expected, actual)
