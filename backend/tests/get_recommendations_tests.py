import unittest
import sample_data
from tracks_model import get_recommendations
from unittest.mock import MagicMock, call


class TestGetRecommendations(unittest.TestCase):
    def test_get_recommendations_no_seeds_returns_empty(self):
        sp_mock = MagicMock()
        sp_mock.recommendations.return_value = {}

        track_seeds_string = ""
        genre_seeds_string = ""
        artist_seeds_string = ""

        expected = {}
        actual = get_recommendations(sp_mock, track_seeds_string, genre_seeds_string, artist_seeds_string)
        self.assertEqual(expected, actual)
        expected_calls = [call.recommendations(seed_genres=None, seed_artists=None,
                                               seed_tracks=None, limit=10)]
        sp_mock.assert_has_calls(expected_calls)

    def test_get_recommendations_two_genre_seeds_check_call(self):
        sp_mock = MagicMock()
        sp_mock.recommendations.return_value = sample_data.recommendations_data

        track_seeds_string = "003vvx7Niy0yvhvHt4a68B;03jhnLcIT8C4DhXnNecOZv;06qEGQMavekDfu9fVsFAMz"
        genre_seeds_string = "hip-hop;rap;pop;k-pop;whatever"
        artist_seeds_string = ""

        expected = {'12345': {
            'artists': [{'external_url': 'artist url', 'name': 'artist name'}],
            'date-created': '1981-12',
            'song_url': "spotify url",
            'song_name': "track name 123",
            'preview_url': "preview url"
        }}
        actual = get_recommendations(sp_mock, track_seeds_string, genre_seeds_string, artist_seeds_string)
        expected_calls = [call.recommendations(seed_genres=['hip-hop', 'rap'], seed_artists=None,
                                               seed_tracks=['003vvx7Niy0yvhvHt4a68B', '03jhnLcIT8C4DhXnNecOZv',
                                                            '06qEGQMavekDfu9fVsFAMz'], limit=10)]
        sp_mock.assert_has_calls(expected_calls)
        self.assertEqual(expected, actual)

    def test_get_recommendations_artists_seed_check_call(self):
        sp_mock = MagicMock()
        sp_mock.recommendations.return_value = {}

        track_seeds_string = ""
        genre_seeds_string = ""
        artist_seeds_string = "abc;def;ghi;jkl;mno;pqr;stu;vwx;yz"

        actual = get_recommendations(sp_mock, track_seeds_string, genre_seeds_string, artist_seeds_string)
        expected_calls = [call.recommendations(seed_genres=None, seed_artists=['abc', 'def', 'ghi', 'jkl', 'mno'],
                                               seed_tracks=None, limit=10)]
        sp_mock.assert_has_calls(expected_calls)
        self.assertEqual({}, actual)
