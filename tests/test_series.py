from unittest import TestCase
from quickplots.series import Series

class SeriesCreationTests(TestCase):

    def test_can_create_series(self):
        series = Series((1, 1), (2, 4), (3, 9))
        self.assertEqual(series._data, [(1, 1), (2, 4), (3, 9)])


    def test_can_create_series_with_list_points(self):
        series = Series([1, 1], (2, 4), [3, 9])
        self.assertEqual(series._data, [(1, 1), (2, 4), (3, 9)])


    def test_points_can_only_be_list_or_tuple(self):
        with self.assertRaises(TypeError):
            Series([1, 1], (2, 4), [3, 9], set([8, 9]))


    def test_point_values_must_be_numeric(self):
        with self.assertRaises(TypeError):
            Series((1, 1), (2, 4), (3, "9"))
        Series((1, 1), (2, 4), (3, 7.8))


    def test_all_points_must_be_of_length_two(self):
        with self.assertRaises(ValueError):
            Series((1, 1), (2, 4), (3, 9), (4, 16, 10))
        with self.assertRaises(ValueError):
            Series((1, 1), (2, 4), (3, 9), (4,))


    '''def test_can_create_series_as_seperate_x_and_y_values(self):
        series = Series((1, 2, 3), (1, 4, 9))
        self.assertEqual(series._data, [(1, 1), (2, 4), (3, 9)])


    def test_data_interpreted_as_xy_points_when_ambiguous(self):
        series = Series((1, 1), (2, 4))
        self.assertEqual(series._data, [(1, 1), (2, 4)])'''
