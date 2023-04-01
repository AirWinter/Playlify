import unittest
from utils import filter_by_date, filter_by_genre


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.songs = [{"date-created": "2022-12-02", "genres": ["rap"], "id": "0vjeOZ3Ft5jvAi9SBFJm1j"},
                      {"date-created": "2017-03-07", "genres": ["french hip hop", "rap conscient"],
                       "id": "3Hd7zBAMMjl5yKcDgPymrp"},
                      {"date-created": "1959-07-01", "genres": ["classic rock", "rock", "rock-and-roll", "rockabilly"],
                       "id": "2QfiRTz5Yc8DdShCxG1tB2"},
                      {"date-created": "2010-05-03", "genres": ["epicore", "soundtrack"],
                       "id": "4JtvyWkWQTPVcroZf8JJkp"},
                      {"date-created": "2021-07-15", "genres": [], "id": "49YUpbAI8RbtiTUg2486Fc"},
                      {"date-created": "1999-06-08", "genres": ["alternative rock", "pop rock"],
                       "id": "3cfOd4CMv2snFaKAnMdnvK"}, {"date-created": "2021-07-23",
                                                         "genres": ["canadian pop punk", "canadian punk",
                                                                    "canadian rock",
                                                                    "pop punk"], "id": "6DD5beNG6Ji3AYp5WrYnwD"},
                      {"date-created": "2006", "genres": [], "id": "1LkoYGxmYpO6QSEvY5C0Zl"},
                      {"date-created": "2017-10-06", "genres": ["hip hop", "pop rap", "rap"],
                       "id": "3i5qVV8azKqGFK4Gzdt5YS"},
                      {"date-created": "2017-10-06", "genres": ["hip hop", "pop rap", "rap"],
                       "id": "07FkzikE6FuHIa8Ma7zJGc"},
                      {"date-created": "2019-07-26", "genres": ["hip hop", "pop rap", "rap"],
                       "id": "5rLyYxZNzca00ENADO9m54"},
                      {"date-created": "2019-07-26", "genres": ["hip hop", "pop rap", "rap"],
                       "id": "3oLe5ZILASG8vU5dxIMfLY"},
                      {"date-created": "2017-10-06", "genres": ["hip hop", "pop rap", "rap"],
                       "id": "52okn5MNA47tk87PeZJLEL"},
                      {"date-created": "2017-10-13", "genres": ["indie anthem-folk", "pop", "uk pop"],
                       "id": "6lOWoTqVnAWXchddtTH31W"},
                      {"date-created": "2022-08-26", "genres": ["big room", "dance pop", "edm", "pop", "pop dance"],
                       "id": "4uUG5RXrOk84mYEfFvj3cK"},
                      {"date-created": "2023-01-13", "genres": ["pop"], "id": "0yLdNVWF3Srea0uzk55zFn"},
                      {"date-created": "1985-06-01",
                       "genres": ["new romantic", "new wave", "new wave pop", "permanent wave", "pop rock", "soft rock",
                                  "synthpop"], "id": "2WfaOiMkCvy7F5fcp2zZ8L"},
                      {"date-created": "1984-02-27", "genres": ["classic rock", "glam rock", "rock"],
                       "id": "1MsBRSbt5dqJSw3RxXtvCM"}, {"date-created": "1989-01-01",
                                                         "genres": ["disco", "europop", "mellow gold", "new romantic",
                                                                    "new wave", "new wave pop", "soft rock",
                                                                    "synthpop"],
                                                         "id": "4NH4xiPQ7TqNGqj6pZV4ki"},
                      {"date-created": "1979", "genres": ["chanson", "french pop"], "id": "4GDdoEUqBhZU5CLrfHppsO"},
                      {"date-created": "1998-01-01", "genres": ["chanson", "french pop"],
                       "id": "5EQid6GG1zk2kz2JCgKoqk"},
                      {"date-created": "2017-12-08", "genres": ["indie rock italiano", "italian pop"],
                       "id": "3Wrjm47oTz2sjIgck11l5e"},
                      {"date-created": "2016-02-18",
                       "genres": ["australian dance", "australian pop", "dance pop", "pop"],
                       "id": "059ACLUOyEcdruA2m9f2jd"}, {"date-created": "2019-07-26",
                                                         "genres": ["covertronica", "dance pop", "edm", "electro house",
                                                                    "pop", "pop dance", "pop edm", "slap house",
                                                                    "tropical house"], "id": "2tnVG71enUj33Ic2nFN6kZ"},
                      {"date-created": "2020-03-11", "genres": ["australian pop", "pop"],
                       "id": "1qCmZnC1FUpNgOydIzqIPC"},
                      {"date-created": "2022-07-21", "genres": ["melodic drill"], "id": "3LtpKP5abr2qqjunvjlX5i"},
                      {"date-created": "2014-09-08", "genres": [], "id": "30CkdHzQnMEI8JvQLkWlP3"},
                      {"date-created": "2006-09-12",
                       "genres": ["adult standards", "bubblegum pop", "disco", "mellow gold", "quiet storm",
                                  "soft rock",
                                  "yacht rock"], "id": "5FMXrphygZ4z3gVDHGWxgl"}, {"date-created": "1999-11-16",
                                                                                   "genres": ["g funk", "gangster rap",
                                                                                              "hip hop", "rap",
                                                                                              "west coast rap"],
                                                                                   "id": "7iXF2W9vKmDoGAhlHdpyIa"}]

    def test_filter_by_genre_rap(self):
        expected = [{'date-created': '2022-12-02',
                     'genres': ['rap'],
                     'id': '0vjeOZ3Ft5jvAi9SBFJm1j'},
                    {'date-created': '2017-10-06',
                     'genres': ['hip hop', 'pop rap', 'rap'],
                     'id': '3i5qVV8azKqGFK4Gzdt5YS'},
                    {'date-created': '2017-10-06',
                     'genres': ['hip hop', 'pop rap', 'rap'],
                     'id': '07FkzikE6FuHIa8Ma7zJGc'},
                    {'date-created': '2019-07-26',
                     'genres': ['hip hop', 'pop rap', 'rap'],
                     'id': '5rLyYxZNzca00ENADO9m54'},
                    {'date-created': '2019-07-26',
                     'genres': ['hip hop', 'pop rap', 'rap'],
                     'id': '3oLe5ZILASG8vU5dxIMfLY'},
                    {'date-created': '2017-10-06',
                     'genres': ['hip hop', 'pop rap', 'rap'],
                     'id': '52okn5MNA47tk87PeZJLEL'},
                    {'date-created': '1999-11-16',
                     'genres': ['g funk', 'gangster rap', 'hip hop', 'rap', 'west coast rap'],
                     'id': '7iXF2W9vKmDoGAhlHdpyIa'}]
        result = filter_by_genre("rap", self.songs)
        self.assertEqual(expected, result)

    def test_filter_by_fake_genre(self):
        expected = []
        result = filter_by_genre("not a genre", self.songs)
        self.assertEqual(expected, result)

    def test_filter_by_date_1978(self):
        expected = [{'date-created': '1979',
                     'genres': ['chanson', 'french pop'],
                     'id': '4GDdoEUqBhZU5CLrfHppsO'}]
        result = filter_by_date("1978", "1980", self.songs)
        self.assertEqual(expected, result)

    def test_filter_by_date_invalid(self):
        with self.assertRaises(ValueError) as context:
            filter_by_date("1979", "1978", self.songs)

            self.assertTrue("Start date has to be before end date" in context.exception)


if __name__ == '__main__':
    unittest.main()
