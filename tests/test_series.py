from unittest import TestCase
from unittest.mock import patch
from quickplots.series import Series
import builtins

class SeriesCreationTests(TestCase):

    def test_can_create_series(self):
        series = Series((1, 1), (2, 4), (3, 9))
        self.assertEqual(series._data, [(1, 1), (2, 4), (3, 9)])
        self.assertEqual(series._name, None)
        self.assertEqual(series._chart, None)


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


    def test_data_will_be_sorted_by_x_value(self):
        series = Series((3, 9), (2, 4), (5, 25), (4, 16))
        self.assertEqual(series._data, [(2, 4), (3, 9), (4, 16), (5, 25)])
        series = Series((2, 3, 4, 5), (4, 9, 16, 25))
        self.assertEqual(series._data, [(2, 4), (3, 9), (4, 16), (5, 25)])


    def test_can_create_series_with_name(self):
        series = Series((1, 1), (2, 4), (3, 9), name="Squares")
        self.assertEqual(series._name, "Squares")


    def test_name_must_be_str(self):
        with self.assertRaises(TypeError):
            Series((1, 1), (2, 4), (3, 9), name=100)


    def test_series_repr(self):
        series = Series((1, 1), (2, 4), (3, 9))
        self.assertEqual(str(series), "<Series (3 data points)>")


    def test_name_in_repr_if_not_none(self):
        series = Series((1, 1), (2, 4), (3, 9), name="Squares")
        self.assertEqual(str(series), "<Series 'Squares' (3 data points)>")



class SeriesPropertyTests(TestCase):

    def test_basic_properties(self):
        series = Series((1, 1), (2, 4), (3, 9), name="Squares")
        self.assertEqual(series.data(), series._data)
        self.assertIs(series.name(), series._name)
        self.assertIs(series.chart(), series._chart)


    def test_series_data_is_read_only(self):
        series = Series((1, 1), (2, 4), (3, 9))
        series.data().append("bad")
        self.assertEqual(series.data(), [(1, 1), (2, 4), (3, 9)])


    def test_can_update_name(self):
        series = Series((1, 1), (2, 4), (3, 9), name="Squares")
        series.name("Sexy squares")
        self.assertEqual(series.name(), "Sexy squares")


    def test_set_name_must_be_str(self):
        series = Series((1, 1), (2, 4), (3, 9), name="Squares")
        with self.assertRaises(TypeError):
            series.name(100)


    def test_can_get_smallest_amd_largest_values(self):
        series = Series((1, -1), (2, 9), (3, 4))
        self.assertEqual(series.smallest_x(), 1)
        self.assertEqual(series.largest_x(), 3)
        self.assertEqual(series.smallest_y(), -1)
        self.assertEqual(series.largest_y(), 9)



class SeriesDataManipulationTests(TestCase):

    def setUp(self):
        self.series = Series((1, 1), (2, 4), (3, 9))


    def test_can_add_data_point(self):
        self.series.add_data_point(4, 16)
        self.assertEqual(self.series.data(), [(1, 1), (2, 4), (3, 9), (4, 16)])


    def test_added_data_must_be_numeric(self):
        with self.assertRaises(TypeError):
            self.series.add_data_point("4", 16)
        with self.assertRaises(TypeError):
            self.series.add_data_point(4, "16")
        self.series.add_data_point(4.1, 16.9)


    def test_new_data_point_will_be_inserted_at_correct_position(self):
        self.series.add_data_point(1.5, 2.25)
        self.assertEqual(self.series.data(), [(1, 1), (1.5, 2.25), (2, 4), (3, 9)])


    @patch("builtins.sorted")
    def test_series_will_not_resort_list_needlessly(self, mock):
        self.series.add_data_point(4, 16)
        self.assertEqual(mock.call_count, 0)


    def test_can_remove_data_point(self):
        self.series.remove_data_point(1, 1)
        self.assertEqual(self.series.data(), [(2, 4), (3, 9)])


    def test_cannot_remove_last_data_point(self):
        self.series.remove_data_point(1, 1)
        self.series.remove_data_point(2, 4)
        with self.assertRaises(ValueError):
            self.series.remove_data_point(3, 9)
