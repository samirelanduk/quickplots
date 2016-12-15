from unittest import TestCase
from quickplots.series import Series

class SeriesCreationTests(TestCase):

    def test_can_create_series(self):
        series = Series((1,1), (2, 4), (3, 9))
        self.assertEqual(series._data, [(1,1), (2, 4), (3, 9)])
