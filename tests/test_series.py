from unittest import TestCase
from unittest.mock import patch
from quickplots.series import Series
from quickplots.charts import AxisChart
import builtins

class SeriesCreationTests(TestCase):

    def test_can_create_series(self):
        series = Series((1, 1), (2, 4), (3, 9))
        self.assertEqual(series._data, [(1, 1), (2, 4), (3, 9)])
        self.assertEqual(series._color, "#000000")
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


    def test_can_create_line_series_with_color(self):
        series = Series((1, 1), (2, 4), (3, 9), color="#FF0000")
        self.assertEqual(series._color, "#FF0000")


    def test_color_must_be_str(self):
        with self.assertRaises(TypeError):
            Series((1, 1), (2, 4), (3, 9), color=100)


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
        self.assertIs(series.color(), series._color)
        self.assertIs(series.name(), series._name)
        self.assertIs(series.chart(), series._chart)


    def test_series_data_is_read_only(self):
        series = Series((1, 1), (2, 4), (3, 9))
        series.data().append("bad")
        self.assertEqual(series.data(), [(1, 1), (2, 4), (3, 9)])


    def test_can_modify_color(self):
        series = Series((1, 1), (2, 4), (3, 9))
        series.color("#00FF00")
        self.assertEqual(series.color(), "#00FF00")


    def test_set_color_must_be_str(self):
        series = Series((1, 1), (2, 4), (3, 9))
        with self.assertRaises(TypeError):
            series.color(100)


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



class SeriesPaintingTests(TestCase):

    def setUp(self):
        x = list(range(1, 11))
        y = [n ** 2 for n in x]
        data = list(zip(x, y))
        self.series = Series(*data)
        self.chart = AxisChart(self.series, width=1000, height=500)


    def test_series_with_no_chart_returns_none_for_canvas_points(self):
        series = Series((1, 1), (2, 4), (3, 9), (4, 16), (5, 25))
        self.assertEqual(series.canvas_points(), None)


    def test_series_can_get_canvas_points_with_zero_base(self):
        self.assertEqual(
         self.series.canvas_points(),
         (
          (180, 446), (260, 434), (340, 414), (420, 386), (500, 350),
          (580, 306), (660, 254), (740, 194), (820, 126), (900, 50)
         )
        )


    def test_series_canvas_points_with_zero_base_with_unusual_margin(self):
        self.chart.horizontal_padding(0.45)
        self.chart.vertical_padding(0.25)
        self.assertEqual(
         self.series.canvas_points(),
         (
          (460, 372.5), (470, 365), (480, 352.5), (490, 335), (500, 312.5),
          (510, 285), (520, 252.5), (530, 215), (540, 172.5), (550, 125)
         )
        )


    def test_non_zero_based_series_points(self):
        self.chart.x_lower_limit(5)
        self.chart.x_upper_limit(15)
        self.chart.y_lower_limit(50)
        self.chart.y_upper_limit(300)
        self.assertEqual(
         self.series.canvas_points(),
         (
          (-220, 528.4), (-140, 523.6), (-60, 515.6), (20, 504.4), (100, 490),
          (180, 472.4), (260, 451.6), (340, 427.6), (420, 400.4), (500, 370)
         )
        )
