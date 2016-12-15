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


    def test_must_be_at_least_one_data_point(self):
        with self.assertRaises(ValueError):
            Series()


    def test_all_points_must_be_of_length_two(self):
        with self.assertRaises(ValueError):
            Series((1, 1), (2, 4), (3, 9), (4, 16, 10))
        with self.assertRaises(ValueError):
            Series((1, 1), (2, 4), (3, 9), (4,))


    def test_can_create_series_as_seperate_x_and_y_values(self):
        series = Series((1, 2, 3), (1, 4, 9))
        self.assertEqual(series._data, [(1, 1), (2, 4), (3, 9)])


    def test_seperate_xy_lists_must_be_of_equal_length(self):
        with self.assertRaises(ValueError):
            Series((1, 2, 3), (1, 4, 9, 16))


    def test_data_interpreted_as_xy_points_when_ambiguous(self):
        series = Series((1, 1), (2, 4))
        self.assertEqual(series._data, [(1, 1), (2, 4)])


    def test_can_provide_xy_lists_as_lists(self):
        series = Series([1, 2, 3], [1, 4, 9])
        self.assertEqual(series._data, [(1, 1), (2, 4), (3, 9)])


    def test_xy_lists_can_only_be_lists_or_tuples(self):
        with self.assertRaises(TypeError):
            Series([1, 2, 3], set([1, 4, 9]))


    def test_xy_list_values_must_be_numeric(self):
        with self.assertRaises(TypeError):
            Series((1, 2, 3), (1, 4, "9"))
        Series((1, 2, 3), (1, 4, 9.5))


    def test_series_repr(self):
        series = Series((1, 1), (2, 4), (3, 9))
        self.assertEqual(str(series), "<Series (3 data points)>")



class SeriesPropertyTests(TestCase):

    def test_basic_properties(self):
        series = Series((1, 1), (2, 4), (3, 9))
        self.assertEqual(series.data(), series._data)


    def test_series_data_is_read_only(self):
        series = Series((1, 1), (2, 4), (3, 9))
        series.data().append("bad")
        self.assertEqual(series.data(), [(1, 1), (2, 4), (3, 9)])
